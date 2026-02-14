# Westfalen Weser Kundenportal for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This is a custom integration for Home Assistant to retrieve electricity consumption and feed-in data from the **Westfalen Weser Kundenportal** (https://www.ww-kundenportal.com).

## Features
-   **Authentication**: Logs in automatically using your portal credentials.
-   **Sensors**: Creates sensors for:
    -   Total Electricity Purchase (Strombezug)
    -   Total Electricity Feed-in (Stromeinspeisung)
-   **Energy Dashboard**: Fully compatible with the Energy Dashboard.
-   **Config Flow**: UI-based configuration (No YAML needed).

## Installation

### Method 1: HACS (Recommended)
1.  Open HACS in Home Assistant.
2.  Go to **Integrations** > Top Right Menu > **Custom repositories**.
3.  Add the URL of this repository.
4.  Category: **Integration**.
5.  Click **Add**.
6.  Find **Westfalen Weser Kundenportal** in the list and install it.
7.  Restart Home Assistant.

### Method 2: Manual
1.  Download the repository.
2.  Copy the `custom_components/ww_kundenportal` directory to your `config/custom_components` directory in Home Assistant.
3.  Restart Home Assistant.

## Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration**.
3.  Search for **Westfalen Weser**.
4.  Enter your username and password for the customer portal.

## Usage

Once configured, the following sensors will be available:
-   `sensor.westfalen_weser_strombezug`
-   `sensor.westfalen_weser_stromeinspeisung`

Use these in your **Energy Dashboard**:
-   **Grid Consumption**: Add `sensor.westfalen_weser_strombezug`
-   **Return to Grid**: Add `sensor.westfalen_weser_stromeinspeisung`

## Disclaimer
This is an unofficial integration and is not affiliated with Westfalen Weser Netz GmbH. Use at your own risk.
