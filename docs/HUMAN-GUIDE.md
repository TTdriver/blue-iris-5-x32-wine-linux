# Install Blue Iris 5 yourself

Use this guide for manual installation. [AI-PROMPT.md](AI-PROMPT.md) is the alternative for an AI-assisted installation. This approach worked in a personal setup; the generalized steps have not been rerun from scratch on a fresh system. Try it at your own risk.

## 1. Install Wine on a Linux desktop

The working system used Zorin OS 18.1 and Wine 10.0. You need Wine with 32-bit support, 7-Zip, ripgrep and a graphical desktop session. Use your distribution's package instructions. On Ubuntu/Zorin, the package commands used were:

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine wine64 wine32:i386 p7zip-full ripgrep
wine --version
```

These package names and the Wine version your repositories provide may differ on other distributions. Run the remaining commands from the root of this repository.

## 2. Create a separate 32-bit prefix

A Wine prefix is the directory holding this application's Windows environment. Use a new directory so this installation stays separate from your other Wine applications.

```bash
export BI_PREFIX="$HOME/.local/share/blueiris-wine"
bash scripts/prepare-prefix.sh "$BI_PREFIX"
export WINEPREFIX="$BI_PREFIX"
```

The helper creates a `win32` prefix. An existing 64-bit prefix cannot be converted by changing `WINEARCH`; choose a new directory instead.

## 3. Install the legacy vendor packages

The working route used the official **Blue Iris 4.8.6.3 installer**, followed by the **Blue Iris 5.9.9.98 32-bit update**. Obtain legitimate copies of those versions. A current BI installer is a different software generation. [TESTED-SETUP.md](TESTED-SETUP.md) identifies the historical packages.

Install version 4 into this prefix, using your actual installer path:

```bash
wine "/path/to/BlueIris-4.8.6.3.exe"
```

Complete the installer and close any application it launches. Extract the version-5 update into its own application directory, then copy the four dependencies from the version-4 installation:

```bash
BI_APP="$BI_PREFIX/drive_c/Program Files/Blue Iris 5"
mkdir -p "$BI_APP"
7z x -y "/path/to/legacy-version-5-update32.exe" "-o$BI_APP"
cp "$BI_PREFIX/drive_c/Program Files/Blue Iris 4/"{SeaMAX.dll,ftd2xx.dll,msvcr120.dll,msvcp120.dll} "$BI_APP/"
```

Replace both placeholder paths with your own files. The working setup placed `BlueIris.exe` and those four DLLs together in `Blue Iris 5`. No custom Wine DLL overrides were needed for this installation.

## 4. Launch Blue Iris 5

```bash
bash scripts/launch-blue-iris.sh "$BI_PREFIX"
```

Dismiss the normal Demo dialog if you are using an evaluation copy, or activate your legitimate license. Confirm that the main application opens. **That completes this guide.** Further application setup is your responsibility.

Keep the graphical desktop session open while BI runs. See [startup troubleshooting](TROUBLESHOOTING.md) if the program does not open, and [script instructions](../scripts/README.md) for log locations.
