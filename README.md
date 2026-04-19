# S3 Bucket Downloader 🚀

A modern, high-performance desktop application built with Python for bulk downloading files from AWS S3 buckets. Featuring a sleek, dark-themed interface and real-time progress tracking.

![S3 Downloader Preview](https://raw.githubusercontent.com/TomSchimansky/CustomTkinter/master/images/customtkinter_logo.png) *(Note: Replace with your own screenshot!)*

## ✨ Features

- **Bulk Download**: Sync entire S3 buckets to your local machine with a single click.
- **Modern UI**: Built using `CustomTkinter` for a professional, dark-mode administrative experience.
- **Directory Mirroring**: Automatically recreates your S3 folder structures locally.
- **Aggregate Progress**: Real-time progress bar and status updates showing exact file-by-file progress.
- **Multithreaded**: The UI remains responsive even during heavy network activity.
- **Secure Handling**: Password-masked fields for sensitive AWS credentials.

## 🛠️ Prerequisites

- **Python 3.7+**
- **AWS Credentials**: Access Key ID and Secret Access Key with appropriate S3 permissions.
- **Xcode CLI Tools** (for macOS users): Required if you need to install dependencies that require compilation.

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/s3-bucket-downloader.git
   cd s3-bucket-downloader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   *Note: If you encounter an Xcode license error on macOS, run `sudo xcodebuild -license` to accept it first.*

## 📖 Usage

1. Launch the application:
   ```bash
   python main.py
   ```
2. Enter your **AWS Access Key ID** and **Secret Access Key**.
3. Select your target **AWS Region**.
4. Enter the name of the **S3 Bucket**.
5. Click **Browse** to select your local download destination.
6. Click **Download All Files** and monitor the progress!

## 🔐 Security Note

> [!CAUTION]
> **Never commit your AWS credentials to Git.** This application is designed for you to enter them locally. For enhanced security, ensure you follow AWS best practices for IAM user permissions (least privilege).

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

---
*Built with ❤️ using Python, CustomTkinter, and Boto3.*
