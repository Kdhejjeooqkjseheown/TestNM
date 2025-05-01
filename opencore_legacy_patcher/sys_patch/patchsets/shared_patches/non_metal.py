"""
non_metal.py: Non-Metal patches
"""

from .base import BaseSharedPatchSet

from ..base import PatchType

from ....datasets.os_data import os_data


class NonMetal(BaseSharedPatchSet):

    def __init__(self, xnu_major: int, xnu_minor: int, marketing_version: str) -> None:
        super().__init__(xnu_major, xnu_minor, marketing_version)


    def _os_requires_patches(self) -> bool:
        """
        Dropped support with macOS 10.14, Mojave
        """
        return self._xnu_major >= os_data.mojave.value


    def patches(self) -> dict:
        """
        General non-Metal GPU patches
        """
        if self._os_requires_patches() is False:
            return {}

        return {
            "Non-Metal Common": {
                PatchType.OVERWRITE_SYSTEM_VOLUME: {
                    "/System/Applications": {
                        **({ "Photo Booth.app": "11.7.9"} if self._xnu_major >= os_data.monterey else {}),
                    },
                    "/usr/sbin": {
                        **({ "screencapture": "14.7"} if self._xnu_major >= os_data.sequoia else {}),
                    },
                    "/System/Library/CoreServices/RemoteManagement": {
                        **({"ScreensharingAgent.bundle": "14.7.2"} if self._xnu_major >= os_data.sequoia else {}),
                        **({"screensharingd.bundle":     "14.7.2"} if self._xnu_major >= os_data.sequoia else {}),
                        **({"SSMenuAgent.app":           "14.7.2"} if self._xnu_major >= os_data.sequoia else {}),
                    },
                },
                PatchType.REMOVE_SYSTEM_VOLUME: {
                    "/System/Library/Extensions": [
                        "AMDRadeonX4000.kext",
                    ],
                    "/System/Library/ExtensionKit/Extensions/": [
                        "WallpaperMacintoshExtension.appex"
                    ],
                },
                PatchType.OVERWRITE_DATA_VOLUME: {
                    "/Library/Application Support/SkyLightPlugins": {
                        **({ "DropboxHack.dylib": "SkyLightPlugins" } if self._xnu_major >= os_data.monterey else {}),
                        **({ "DropboxHack.txt":   "SkyLightPlugins" } if self._xnu_major >= os_data.monterey else {}),
                    },
                },
                PatchType.MERGE_SYSTEM_VOLUME: {
                    "/System/Library/Frameworks": {
                        "OpenGL.framework":       "10.14.3",
                        "CoreDisplay.framework": f"10.14.4-{self._xnu_major}",
                        "QuartzCore.framework":  f"10.15.7-{self._xnu_major}",
                    },
                    "/System/Library/PrivateFrameworks": {
                        "GPUSupport.framework": "10.14.3",
                        "SkyLight.framework":  f"10.14.6-{self._xnu_major}",
                        **({"FaceCore.framework":  f"13.5"} if self._xnu_major >= os_data.sonoma else {}),
                    },
                },
                PatchType.EXECUTE: {
                    # 'When Space Allows' option introduced in 12.4 (XNU 21.5)
                    **({"/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist ShowDate -int 1": True } if self._xnu_float >= self.macOS_12_4 else {}),
                    "/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist InternalDebugUseGPUProcessForCanvasRenderingEnabled -bool false": True,
                    "/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist WebKitExperimentalUseGPUProcessForCanvasRenderingEnabled -bool false": True,
                    **({"/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist WebKitPreferences.acceleratedDrawingEnabled -bool false": True} if self._xnu_major >= os_data.sonoma else {}),
                    **({"/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist NSEnableAppKitMenus -bool false": True} if self._xnu_major >= os_data.sonoma else {}),
                    **({"/usr/bin/defaults write /Library/Preferences/.GlobalPreferences.plist NSZoomButtonShowMenu -bool false": True} if self._xnu_major == os_data.sonoma else {}),
                },
            },
        }
