# rEFInd Bazzite Pneaple

A 4K neon-gaming-room rEFInd theme, combining **Pneaple-inspired translucent black header/menu/footer bands** with MIT-licensed refindTTT transparency icons and matching blue selection backgrounds. Built around the Bazzite gaming experience and rEFInd 0.14.x.

> **Status:** First installation candidate. Image dimensions and transparency are verified, but its on-screen position and behavior have **not yet been tested on physical UEFI firmware**. The example preview is a **concept illustration**, not an actual rEFInd capture.

![Illustrative theme concept (not a firmware screenshot)](screenshots/concept-preview.png)

## Included assets

- `background.png`: **3840×2160 RGB PNG**, resampled from the approved 1672×941 illustration, including the header and *empty* translucent menu/tool bands.
- `selection_big.png` / `selection_small.png`: **288×288 / 160×160 RGBA PNG** imported from refindTTT for 256px OS / 120px tool icons.
- `icons/os_bazzite.png`, `os_win.png`, `os_windows.png`, and `os_win11.png`: original MIT-licensed refindTTT icon PNGs (with the Windows aliases pointing to the same artwork).
- `icons/func_firmware.png`, `icons/func_reset.png`, `icons/func_shutdown.png`, `icons/tool_shell.png`, and `icons/tool_rescue.png`: original refindTTT 120px utility icons.
- `icons/os_shell.png` and `icons/os_rescue.png` are retained custom 256px optional/manual-entry icons, since upstream provides Shell and Rescue only as smaller tools. A Shell or Rescue entry **requires a real executable**; adding an icon alone does not create a menu entry.
- `source/`: original generated high-resolution assets for later edits. (Not included in compact install ZIP.)

## refindTTT icon update — experimental

This revision uses the **actual refindTTT icon and selection files**, not AI-generated lookalikes. It imports Bazzite, Windows, firmware, reset, shutdown, Shell-tool and Rescue-tool artwork; its blue selection backgrounds are specifically matched to the transparent-label icons.

Stock rEFInd's selected-entry label is hidden by the theme to prevent double labels. The imported main-menu labels are transparent and become visible with the matching selection background.

**Contrast caveat:** upstream refindTTT warns that its special transparency behaves best against a completely black center background. We have **not altered the approved translucent gaming-room wallpaper**; some lettering may be hard to read until tested on actual 4K UEFI firmware. If necessary, darken just the middle band after capturing an actual boot screenshot.

The theme only changes UI visuals; it does not touch the Fedora Shim loader, Secure Boot keys, boot entry scanning, or NVRAM. The existing custom Shell and Rescue 256px main-row icons are retained because refindTTT only provides them in the 120px tools set.

Source: https://github.com/gutlessCGH/refindTTT
Revision: 427f62a44a701bc75e2fbe973424a2a601238c37
License: Copyright (c) 2026 gutlessCGH, MIT — full text in third_party/refindTTT-LICENSE.

## Install — never replace your bootloader

Prerequisites: an existing, functioning rEFInd installation and an EFI System Partition mounted at `/boot/efi`. Tested *file layout* only; boot-tested by user is still required.

1. Save a backup of your **existing configuration** somewhere off the ESP:

   ```sh
   cp /boot/efi/EFI/refind/refind.conf "$HOME/refind.conf.before-pneaple.bak"
   ```

2. From a checkout of this repository (or from the ZIP root containing the theme folder), copy **only the theme directory** into rEFInd's themes:

   ```sh
   sudo mkdir -p /boot/efi/EFI/refind/themes
   sudo cp -a rEFInd-bazzite-pneaple /boot/efi/EFI/refind/themes/
   ```

   If you cloned the repository, run the copy command **from its parent directory**, or use `sudo cp -a ./ /boot/efi/EFI/refind/themes/rEFInd-bazzite-pneaple/` from the clone after ensuring the destination is a new directory. Do not copy files over another installed theme.

3. Edit `/boot/efi/EFI/refind/refind.conf`. **Replace** the previous theme's final `include themes/.../theme.conf` line (e.g., `themes/rEFInd-ublue/theme.conf`) rather than appending multiple theme includes:

   ```conf
   include themes/rEFInd-bazzite-pneaple/theme.conf
   ```

   Leave your boot stanzas, `scanfor`, `default_selection`, `use_nvram`, EFI paths, and firmware boot order unchanged.

4. For a manually defined Bazzite entry, edit the existing **working** entry to specify the theme icon. **Do not create a duplicate entry or replace your working Shim loader.** For example, an existing Bazzite Shim entry should *retain* this boot chain:

   ```conf
   menuentry "Bazzite (Secure Boot via Shim)" {
       icon /EFI/refind/themes/rEFInd-bazzite-pneaple/icons/os_bazzite.png
       volume 4356a928-b0df-4532-bfcc-8a8b44e96e78
       loader /EFI/fedora/shimx64.efi
   }
   ```

   The volume GUID above is **specific to the author's Bazzite machine** and must not be copied blindly to another computer.

5. Reboot to inspect the actual appearance. In stock rEFInd, menu icon *positions* are not arbitrary and only the **selected** OS's label is generally displayed; the concept preview's permanent multi-label row and large Rescue button are illustrative. If the bands miss the menu rows, edit the background instead of changing your bootloader logic.

### Optional tool row

`showtools` controls utility visibility. If you want firmware, reboot, and shutdown buttons, put the following in your **main `refind.conf`** (not this theme):

```conf
showtools firmware,reboot,shutdown
```

To show the EFI Shell in the utility row as well, add `shell` to `showtools`. If you instead choose to make a **manual main-row Shell menuentry**, ensure its loader is a real trusted executable such as `/shellx64.efi` on the right ESP and that it boots with your Secure Boot configuration. Do not alter the working Fedora Shim loader to point to the shell.

### Rescue Tools

`icons/os_rescue.png` is intentionally a graphic **only**. There is no universal built-in `Rescue Tools` launcher. Do not display it as a functional entry without a real EFI executable or an appropriate firmware entry.

## Revert

Replace the new `include` with your previous theme include, or restore your saved `refind.conf` backup. Because this package changes no `.efi` executables, Secure Boot keys, boot order, or existing loader binaries, reversion is a configuration-only change. The old theme folder should be left intact until your new appearance is verified.

## Notes and limitations

- rEFInd 0.14.1 supports `banner_scale fillscreen`, `icons_dir`, icon sizes, and selection images. Files are validated as RGB/RGBA PNGs, but the first firmware boot is the definitive rendering test.
- Theme images cannot independently control rEFInd text placement, menu height, or guaranteed menu entries; their visual placement is dependent on GOP screen mode, the number of entries and version.
- Original wallpaper was generated at 1672×941 and **upscaled**, not natively rendered at 4K.
- Windows naming is supported by common aliases. Bazzite's manual boot entry requires its explicit `icon` directive.
- No changes to Secure Boot binaries or signing are needed for *images*. UEFI executables you launch still need appropriate trust/signing.

## Rebuilding and GitHub publication

Run `python scripts/build_assets.py` to rebuild the 4K wallpaper and the two retained custom main-row icons (requires Pillow). This script deliberately **preserves the imported icons and selection PNGs**. To reproduce the pinned upstream refindTTT import, run `python scripts/sync_refindttt_icons.py` with network access; it verifies upstream Git blob hashes.

## Source wallpaper: Bazzite Convergence

The neon gaming-room background was adapted and recomposed from **Convergence**, an **official Bazzite desktop wallpaper**. The installed `background.png` is a user-approved *edited, resampled theme composition* with custom translucent menu bands, not an unmodified copy of the official wallpaper.

- Official source: [Bazzite Convergence wallpaper (press kit)](https://github.com/ublue-os/bazzite/blob/main/press_kit/art/Convergence_Wallpaper.png).
- Also distributed through [Universal Blue artwork / Bazzite wallpapers](https://github.com/ublue-os/artwork/tree/main/wallpapers/bazzite/images).
- Branding guidance: [Bazzite press-kit README](https://github.com/ublue-os/bazzite/blob/main/press_kit/README.md), which asks that official logos not be distorted or modified.

**Licensing note:** The Universal Blue artwork repository declares Apache-2.0 for the repository while cautioning that individual wallpapers can have different licensing. We have not independently verified a file-specific license grant for **Convergence** or whether all incorporated source models permit redistribution of this derivative wallpaper. Being bundled with Bazzite does not, by itself, resolve that question. Confirm redistribution and derivative permissions with the rights holder before treating this artwork as unconditionally reusable. The project's own MIT license covers its original code and documentation, **not automatically the source wallpaper or official trademarks**.

This is an **unofficial community rEFInd theme**, not affiliated with, sponsored by, or endorsed by Bazzite or Universal Blue. Project and platform names, logos, and other trademarks remain with their respective owners.

## Credits and licensing

Design inspired by [Pneaple Boot Theme by pineapplelite](https://github.com/pineapplelite/Pneaple-Boot-Theme) (MIT-licensed) and icon-shadow treatment inspired by [BsxM1 by AlexFullmoon](https://github.com/AlexFullmoon/refind-bsxm1-theme). This version **includes original refindTTT PNGs** by gutlessCGH under MIT; see `third_party/refindTTT-LICENSE` and `ATTRIBUTION.md`. The gaming-room artwork and the retained Shell/Rescue main-row icons were independently generated from the approved concepts. Bazzite, Windows and other names/logos remain the property of their respective holders; not an official Bazzite/Universal Blue release. See `LICENSE` and `ATTRIBUTION.md`.

Official documentation: [rEFInd Theming](https://www.rodsbooks.com/refind/themes.html) and [rEFInd Configuration](https://www.rodsbooks.com/refind/configfile.html).
