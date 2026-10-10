# Installation and startup troubleshooting

Use this page only when installation or launching fails. [HUMAN-GUIDE.md](HUMAN-GUIDE.md) contains the installation steps.

## Wine is missing or prefix creation fails

Check `wine --version`. Verify that your distribution's Wine packages and 32-bit support are installed. Read the `wineboot` error before retrying. Run from a graphical desktop session.

## Wrong prefix architecture

This guide requires `win32`. Check the prefix's `system.reg` for its `#arch=` line. Changing `WINEARCH` does not convert an existing prefix. Create a separate prefix with the required architecture.

## Application not found

Replace placeholder installer paths with your real filenames. Confirm that the installation or extraction created `BlueIris.exe` in the directory specified in the human guide. Run the helper with the same prefix you used for installation.

## Application exits during startup

Check that the extracted BI 5 executable and all four DLLs from the BI 4 installation are in `C:\Program Files\Blue Iris 5`. The update must be the legacy 32-bit build.

Check the launch log at `~/.local/state/blueiris-wine/blueiris.log`, or under `XDG_STATE_HOME` if set. For more detail, reproduce the launch from a terminal using the same prefix and DLL overrides with Wine debugging enabled. Keep logs local: they may contain private information.

Use [TESTED-SETUP.md](TESTED-SETUP.md) to compare installed versions. A different BI release, Wine build or DLL set is an unverified combination.

## Demo dialog or desktop session

Dismiss the normal evaluation dialog yourself, or activate your legitimate license. Keep the graphical session hosting BI open. A desktop launcher does not provide unattended or headless operation.
