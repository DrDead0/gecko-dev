// |reftest| shell-option(--enable-promise-try) skip-if(!Promise.try||!xulRuntime.shell) -- promise-try is not enabled unconditionally, requires shell-options
// Copyright (C) 2024 Jordan Harband. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
description: >
  Promise.try does not implement [[Construct]], is not new-able
includes: [isConstructor.js]
features: [Reflect.construct, promise-try]
---*/

assert.sameValue(isConstructor(Promise.try), false, 'isConstructor(Promise.all) must return false');

assert.throws(TypeError, function () {
  new Promise.try(function () {});
});


reportCompare(0, 0);
