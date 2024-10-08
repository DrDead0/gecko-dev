/*
 * This file contains tests for the Preferences search bar.
 */

/**
 * Test for searching for the "Saved Logins" subdialog.
 */
add_task(async function () {
  await openPreferencesViaOpenPreferencesAPI("paneGeneral", {
    leaveOpen: true,
  });
  await evaluateSearchResults("sites are stored", "passwordsGroup");
  BrowserTestUtils.removeTab(gBrowser.selectedTab);
});

/**
 * Test for searching for the "Exceptions - Enhanced Tracking Protection" subdialog:
 * "You can specify which websites have Enhanced Tracking Protection turned off." #permissions-exceptions-manage-etp-desc
 */
add_task(async function () {
  await openPreferencesViaOpenPreferencesAPI("paneGeneral", {
    leaveOpen: true,
  });
  await evaluateSearchResults(
    "Enhanced Tracking Protection turned off",
    "trackingGroup"
  );
  BrowserTestUtils.removeTab(gBrowser.selectedTab);
});
