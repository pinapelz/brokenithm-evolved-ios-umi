# Brokenithm-Evolved-iOS-Umi

A version of [esterTion/Brokenithm-iOS](https://github.com/esterTion/Brokenithm-iOS) but maps inputs to keybinds. Uses a WIRED connection with usbmux

Has support for slider LEDs via websockets ([Umiguri LED Controller Protocol](https://gist.github.com/inonote/00251fed881a82c9df1e505eef1722bc)) so you can get glowy lights if its supported (port 7124)

[![Demo](https://files.catbox.moe/w3564o.png)](https://files.catbox.moe/oz9kos.mp4)

# Usage
You will should first download an iOS client/app. Some options are listed below:
- [OWCramer/Brokenithm-SwiftUI](https://github.com/OWCramer/Brokenithm-SwiftUI) - Shown in demo image. Build from source and sideload the IPA OR Join the TestFlight on the repo's README
- [esterTion/Brokenithm-iOS](https://github.com/esterTion/Brokenithm-iOS) - Build from source or download the IPA [here](https://redive.estertion.win/ipas/Brokenithm-iOS-build-10.ipa) ([backup](https://files.catbox.moe/3zhhn2.ipa)) then sideload

Download the latest built version from Releases. Extract the files into some folder, you should keep all the files in the ZIP together.

Run `Brokenithm-Evolved-iOS-Umi.exe`

**Ensure that UMIGURI is sending LED data on port 7124**

> [!IMPORTANT]  
> You must launch the server before Umiguri. If Umiguri is already opened you will need to restart the game. 

