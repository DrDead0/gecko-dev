/* Any copyright is dedicated to the Public Domain.
 * http://creativecommons.org/publicdomain/zero/1.0/
 */

/* Application in use complete MAR file staged patch apply success test */

async function run_test() {
  if (!setupTestCommon()) {
    return;
  }
  const STATE_AFTER_STAGE = STATE_APPLIED;
  gTestFiles = gTestFilesCompleteSuccess;
  const channelPrefs = getTestFileByName(FILE_CHANNEL_PREFS);
  if (channelPrefs) {
    channelPrefs.originalContents = null;
    channelPrefs.compareContents = "FromComplete\n";
    channelPrefs.comparePerms = 0o644;
  }
  gTestDirs = gTestDirsCompleteSuccess;
  await setupUpdaterTest(FILE_COMPLETE_MAR, true);
  setupSymLinks();
  await runHelperFileInUse(DIR_MACOS + gCallbackBinFile, false);
  await stageUpdate(STATE_AFTER_STAGE, true);
  checkPostUpdateRunningFile(false);
  checkFilesAfterUpdateSuccess(getStageDirFile, true);
  checkUpdateLogContents(LOG_COMPLETE_SUCCESS, true);
  // Switch the application to the staged application that was updated.
  runUpdate(STATE_SUCCEEDED, true, 0, true);
  await waitForHelperExit();
  await checkPostUpdateAppLog();
  checkAppBundleModTime();
  checkSymLinks();
  await testPostUpdateProcessing();
  checkPostUpdateRunningFile(true);
  checkFilesAfterUpdateSuccess(getApplyDirFile);
  checkUpdateLogContents(LOG_REPLACE_SUCCESS, false, true);
  await waitForUpdateXMLFiles();
  await checkUpdateManager(STATE_NONE, false, STATE_SUCCEEDED, 0, 1);
  checkCallbackLog();
}

/**
 * Setup symlinks for the test.
 */
function setupSymLinks() {
  if (AppConstants.platform == "macosx" || AppConstants.platform == "linux") {
    removeSymlink();
    createSymlink();
    registerCleanupFunction(removeSymlink);
    gTestFiles.splice(gTestFiles.length - 3, 0, {
      description: "Readable symlink",
      fileName: "link",
      relPathDir: DIR_RESOURCES,
      originalContents: "test",
      compareContents: "test",
      originalFile: null,
      compareFile: null,
      originalPerms: 0o666,
      comparePerms: 0o666,
    });
  }
}

/**
 * Checks the state of the symlinks for the test.
 */
function checkSymLinks() {
  if (AppConstants.platform == "macosx" || AppConstants.platform == "linux") {
    checkSymlink();
  }
}
