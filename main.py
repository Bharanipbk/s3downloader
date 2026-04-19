import os
import threading
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set appearance and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class S3DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("S3 Bucket Downloader")
        self.geometry("600x650")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.label_title = ctk.CTkLabel(self.main_frame, text="S3 Bucket Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.label_subtitle = ctk.CTkLabel(self.main_frame, text="All files from the bucket will be downloaded.", font=ctk.CTkFont(size=14))
        self.label_subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Credentials Section
        self.cred_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cred_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.cred_frame.grid_columnconfigure(1, weight=1)

        self.entry_access_key = self.create_input(self.cred_frame, "Access Key ID:", 0)
        self.entry_secret_key = self.create_input(self.cred_frame, "Secret Access Key:", 1, show="*")
        
        # Region Selection
        self.label_region = ctk.CTkLabel(self.cred_frame, text="Region:", anchor="w")
        self.label_region.grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        self.option_region = ctk.CTkOptionMenu(self.cred_frame, values=["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "ap-south-1"])
        self.option_region.grid(row=2, column=1, padx=0, pady=10, sticky="ew")
        self.option_region.set("us-east-1")

        # File Section
        self.file_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.file_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.entry_bucket = self.create_input(self.file_frame, "S3 Bucket Name:", 0)

        # Destination Selection
        self.dest_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.dest_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.dest_frame.grid_columnconfigure(1, weight=1)

        self.label_dest = ctk.CTkLabel(self.dest_frame, text="Save To:", anchor="w")
        self.label_dest.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.entry_dest_path = ctk.CTkEntry(self.dest_frame, placeholder_text="Choose destination folder...")
        self.entry_dest_path.grid(row=0, column=1, padx=0, pady=10, sticky="ew")
        
        self.btn_browse = ctk.CTkButton(self.dest_frame, text="Browse", width=80, command=self.browse_destination)
        self.btn_browse.grid(row=0, column=2, padx=(10, 0), pady=10)

        # Progress Section
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, orientation="horizontal")
        self.progress_bar.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

        self.label_status = ctk.CTkLabel(self.main_frame, text="Ready", font=ctk.CTkFont(size=12))
        self.label_status.grid(row=6, column=0, padx=20, pady=(0, 10))

        # Download Button
        self.btn_download = ctk.CTkButton(self.main_frame, text="Download All Files", height=45, font=ctk.CTkFont(weight="bold"), command=self.start_download)
        self.btn_download.grid(row=7, column=0, padx=20, pady=(20, 30), sticky="ew")

    def create_input(self, parent, label_text, row, show=None):
        label = ctk.CTkLabel(parent, text=label_text, anchor="w")
        label.grid(row=row, column=0, padx=(0, 10), pady=10, sticky="w")
        entry = ctk.CTkEntry(parent, show=show)
        entry.grid(row=row, column=1, padx=0, pady=10, sticky="ew")
        return entry

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_dest_path.delete(0, "end")
            self.entry_dest_path.insert(0, folder)

    def update_status(self, text, progress=None):
        self.label_status.configure(text=text)
        if progress is not None:
            self.progress_bar.set(progress)

    def start_download(self):
        # Validate inputs
        access_key = self.entry_access_key.get()
        secret_key = self.entry_secret_key.get()
        bucket = self.entry_bucket.get()
        dest_folder = self.entry_dest_path.get()
        region = self.option_region.get()

        if not all([access_key, secret_key, bucket, dest_folder]):
            messagebox.showwarning("Incomplete Fields", "Please fill in all fields.")
            return

        # Disable button during download
        self.btn_download.configure(state="disabled")
        self.update_status("Scanning bucket...", 0.05)

        # Run download in a separate thread
        thread = threading.Thread(target=self.download_worker, args=(access_key, secret_key, region, bucket, dest_folder))
        thread.daemon = True
        thread.start()

    def download_worker(self, access_key, secret_key, region, bucket, dest_folder):
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )

            # List all objects in the bucket
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket)

            all_objects = []
            total_size = 0
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        all_objects.append(obj)
                        total_size += obj['Size']

            if not all_objects:
                self.update_status("Bucket is empty.")
                messagebox.showinfo("Empty", "The selected bucket is empty.")
                return

            total_files = len(all_objects)
            downloaded_bytes = 0
            
            for i, obj in enumerate(all_objects):
                s3_key = obj['Key']
                # Skip folders (keys ending in /)
                if s3_key.endswith('/'):
                    continue

                local_path = os.path.join(dest_folder, s3_key)
                local_dir = os.path.dirname(local_path)
                
                # Create local directories if they don't exist
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)

                self.update_status(f"Downloading {i+1}/{total_files}: {os.path.basename(s3_key)}", 
                                  (downloaded_bytes/total_size) if total_size > 0 else 0)

                # Progress callback for individual file
                def progress_callback(bytes_amount):
                    nonlocal downloaded_bytes
                    downloaded_bytes += bytes_amount
                    progress = (downloaded_bytes / total_size) if total_size > 0 else 1
                    self.update_status(f"Downloading... {int(progress*100)}%", progress)

                s3.download_file(bucket, s3_key, local_path, Callback=progress_callback)

            self.update_status("All downloads complete!", 1.0)
            messagebox.showinfo("Success", f"Successfully downloaded {total_files} files.")

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'NoSuchBucket':
                msg = "The specified bucket does not exist."
            elif error_code == '403':
                msg = "Access denied. Check your credentials and bucket permissions."
            else:
                msg = str(e)
            self.update_status("Error occurred.")
            messagebox.showerror("AWS Error", msg)
        except Exception as e:
            self.update_status("Error occurred.")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            self.btn_download.configure(state="normal")

if __name__ == "__main__":
    app = S3DownloaderApp()
    app.mainloop()
