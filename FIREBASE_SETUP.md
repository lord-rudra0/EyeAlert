# Firebase Setup Guide for EyeAlert

Follow these steps to connect your EyeAlert system to the cloud.

## Step 1: Create a Firebase Project
1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Click **"Add project"**.
3.  Name it (e.g., `EyeAlert-Monitor`) and click **Continue**.
4.  Disable Google Analytics (not needed for this) and click **Create project**.

## Step 2: Create the Database
1.  In the left sidebar, click **Build** -> **Realtime Database**.
2.  Click **Create Database**.
3.  Choose a location (e.g., United States) and click **Next**.
4.  **Crucial Step**: Choose **Start in Test Mode**.
    *   *Warning: This allows anyone to read/write for 30 days. For production, you'd set up rules, but for now, this is easiest.*
5.  Click **Enable**.
6.  **Copy the URL**: At the top of the Data tab, you will see a link like `https://eyealert-monitor-default-rtdb.firebaseio.com/`. **Copy this.**

## Step 3: Get the Service Key
1.  Click the **Gear Icon** ⚙️ (Project Settings) at the top left.
2.  Go to the **Service accounts** tab.
3.  Click **Generate new private key**.
4.  Click **Generate key**.
5.  A file will download (e.g., `eyealert-monitor-firebase-adminsdk-xxxxx.json`).

## Step 4: Connect to EyeAlert
1.  **Rename**: Rename the downloaded file to `serviceAccountKey.json`.
2.  **Move**: Drag and drop this file into your project folder (`d:\Nandhu\Projects\EyeAlert`).
3.  **Update Code**:
    *   Open `firebase_manager.py`.
    *   Find the line: `'databaseURL': 'https://YOUR-PROJECT-ID.firebaseio.com/'`
    *   Replace the URL with the one you copied in Step 2.

## Step 5: View Your Data
1.  Run `python main.py`.
2.  Simulate "Sleeping" (close eyes).
3.  Go back to your Firebase Console -> **Realtime Database**.
4.  You will see a new green folder called `alerts` appear instantly with your data!
