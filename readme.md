# Razer Kraken Headset Keep-Alive Service

## Overview

This repository provides a solution for a known issue with the Razer Kraken Headset, where the headset may go to sleep and cut off audio due to inactivity. The project includes:

- A Rust application that continuously plays an unnoticeable sound file to keep the headset active.
- A Python-based tray application that installs and manages the Rust application as a Windows service.

## Features

- **Keeps Razer Kraken Headset Active:** The Rust executable plays a sound file repeatedly to prevent the headset from going to sleep.
- **Windows Service Integration:** The Rust application is installed as a Windows service to ensure it runs in the background.
- **Tray Application Management:** A Python tray application allows users to manage the Windows service easily, including starting and stopping the service.

## Installation and Setup

### Prerequisites

- **Python:** Required for the tray application. Ensure you have Python installed on your system.
- **Rust:** Required to build the Rust application. Install Rust from [rust-lang.org](https://www.rust-lang.org/).
- **Cargo:** Rust's package manager and build tool, which is typically installed with Rust.

### 1. Building the Rust Application

1. Clone the repository:

    ```sh
    git clone https://github.com/KasperHolck/RazerSoundService.git
    cd your-repo-name
    ```

2. Navigate to the Rust application directory:

3. Build the Rust application:

    ```sh
    cargo build --release
    ```

4. The compiled executable will be located in `target/release/`.

### 2. Setting Up the Python Tray Application

1. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

2. Press [CTRL] + [SHIFT] + B to build the tray application

3. A dist folder will be created with the tray executable inside. Don't run it yet.

### 3. Packaging

1. From the rust release folder move the rust executable into dist/dependencies/server.dist/

2. Install [NSSM](https://nssm.cc/download) and move the executable into dist/dependencies

3. Drag the dist folder onto the desktop

4. Run the dist/dependencies/tray.dist/RazerSoundServiceTray.exe

5. A folder will open, drag the whole dist folder into there

6. Run the ./dist/dependencies/tray.dist/RazerSoundServiceTray.exe again as administrator.

7. For ease of use create a shortcut to this executable and place to desktop.

## Usage

1. Once the tray application is running, you will see an icon in the system tray.
2. Right-click the tray icon and mouse over "Service" and select "Install". 