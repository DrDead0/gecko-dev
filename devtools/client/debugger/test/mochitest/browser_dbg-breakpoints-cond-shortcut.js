/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at <http://mozilla.org/MPL/2.0/>. */

// Test opening conditional panel using keyboard shortcut.
// Should access the closest breakpoint to a passed in cursorPosition.

"use strict";

add_task(async function () {
  const dbg = await initDebugger("doc-scripts.html", "long.js");

  await selectSource(dbg, "long.js");
  await waitForSelectedSource(dbg, "long.js");

  info(
    "toggle conditional panel with shortcut: no breakpoints, default cursorPosition"
  );
  pressKey(dbg, "toggleCondPanel");
  await waitForConditionalPanelFocus(dbg);
  ok(
    !!getConditionalPanel(dbg, 1),
    "conditional panel panel is open on line 1"
  );
  is(
    dbg.selectors.getConditionalPanelLocation().line,
    1,
    "conditional panel location is line 1"
  );
  info("close conditional panel");
  pressKey(dbg, "Escape");

  info(
    "toggle conditional panel with shortcut: cursor on line 32, no breakpoints"
  );
  // codemirror editor offset: cursorPosition will be line + 1, column + 1
  setEditorCursorAt(dbg, 31, 1);
  pressKey(dbg, "toggleCondPanel");

  await waitForConditionalPanelFocus(dbg);
  ok(!!getConditionalPanel(dbg, 32), "conditional panel is open on line 32");
  is(
    dbg.selectors.getConditionalPanelLocation().line,
    32,
    "conditional panel location is line 32"
  );
  info("close conditional panel");
  pressKey(dbg, "Escape");

  info("add active column breakpoint on line 32 and set cursorPosition");
  await enableFirstBreakpoint(dbg);
  setEditorCursorAt(dbg, 31, 1);
  info(
    "toggle conditional panel with shortcut and add condition to first breakpoint"
  );
  setConditionalBreakpointWithKeyboardShortcut(dbg, "1");
  await waitForCondition(dbg, 1);
  const firstBreakpoint = findColumnBreakpoint(dbg, "long.js", 32, 2);
  is(
    firstBreakpoint.options.condition,
    "1",
    "first breakpoint created with condition using shortcut"
  );

  info("set cursor at second breakpoint position and activate breakpoint");
  setEditorCursorAt(dbg, 31, 25);

  await enableSecondBreakpoint(dbg);
  info(
    "toggle conditional panel with shortcut and add condition to second breakpoint"
  );
  setConditionalBreakpointWithKeyboardShortcut(dbg, "2");
  await waitForCondition(dbg, 2);
  const secondBreakpoint = findColumnBreakpoint(dbg, "long.js", 32, 26);
  is(
    secondBreakpoint.options.condition,
    "2",
    "second breakpoint created with condition using shortcut"
  );

  info(
    "set cursor position near first breakpoint, toggle conditional panel and edit breakpoint"
  );
  setEditorCursorAt(dbg, 31, 7);
  info("toggle conditional panel and edit condition using shortcut");
  setConditionalBreakpointWithKeyboardShortcut(dbg, "2");
  ok(
    !!waitForCondition(dbg, "12"),
    "breakpoint closest to cursor position has been edited"
  );

  info("close conditional panel");
  pressKey(dbg, "Escape");

  info(
    "set cursor position near second breakpoint, toggle conditional panel and edit breakpoint"
  );
  setEditorCursorAt(dbg, 31, 21);
  info("toggle conditional panel and edit condition using shortcut");
  setConditionalBreakpointWithKeyboardShortcut(dbg, "3");
  ok(
    !!waitForCondition(dbg, "13"),
    "breakpoint closest to cursor position has been edited"
  );

  info("close conditional panel");
  pressKey(dbg, "Escape");

  info("toggle log panel with shortcut: cursor on line 33");

  setEditorCursorAt(dbg, 33, 1);
  setLogBreakpointWithKeyboardShortcut(dbg, "3");
  ok(
    !!waitForLog(dbg, "3"),
    "breakpoint closest to cursor position has been edited"
  );

  info("close conditional panel");
  pressKey(dbg, "Escape");
});

// from test/mochitest/browser_dbg-breakpoints-cond-source-maps.js
function getConditionalPanel(dbg, line) {
  return getCM(dbg).doc.getLineHandle(line - 1).widgets[0];
}

// from devtools browser_dbg-breakpoints-cond-source-maps.js
async function waitForConditionalPanelFocus(dbg) {
  await waitFor(() => dbg.win.document.activeElement.tagName === "TEXTAREA");
}

// from browser_dbg-breakpoints-columns.js
async function enableFirstBreakpoint(dbg) {
  setEditorCursorAt(dbg, 32, 0);
  await addBreakpoint(dbg, "long.js", 32);
  const bpMarkers = await waitForAllElements(dbg, "columnBreakpoints");

  Assert.strictEqual(bpMarkers.length, 2, "2 column breakpoints");
  assertClass(bpMarkers[0], "active");
  assertClass(bpMarkers[1], "active", false);
}

async function enableSecondBreakpoint(dbg) {
  let bpMarkers = await waitForAllElements(dbg, "columnBreakpoints");

  bpMarkers[1].click();
  await waitForBreakpointCount(dbg, 2);

  bpMarkers = findAllElements(dbg, "columnBreakpoints");
  assertClass(bpMarkers[1], "active");
  await waitForAllElements(dbg, "breakpointItems", 2);
}

// modified method from browser_dbg-breakpoints-columns.js
// use shortcut to open conditional panel.
function setConditionalBreakpointWithKeyboardShortcut(dbg, condition) {
  pressKey(dbg, "toggleCondPanel");
  typeInPanel(dbg, condition);
}

function setLogBreakpointWithKeyboardShortcut(dbg, condition) {
  pressKey(dbg, "toggleLogPanel");
  typeInPanel(dbg, condition, true);
}
