import WebIDL


def WebIDLTest(parser, harness):
    parser.parse(
        """
        [SecureContext]
        interface TestSecureContextOnInterface {
          const octet TEST_CONSTANT = 0;
          readonly attribute byte testAttribute;
          undefined testMethod(byte foo);
        };
        partial interface TestSecureContextOnInterface {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        6,
        "TestSecureContextOnInterface should have six members",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext"),
        "Interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to constant members",
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to attribute members",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to method members",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to "
            "constant members from partial interface"
        ),
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to "
            "attribute members from partial interface"
        ),
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to method members from partial interface",
    )

    # Same thing, but with the partial interface specified first:
    parser = parser.reset()
    parser.parse(
        """
        partial interface TestSecureContextOnInterfaceAfterPartialInterface {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
        [SecureContext]
        interface TestSecureContextOnInterfaceAfterPartialInterface {
          const octet TEST_CONSTANT = 0;
          readonly attribute byte testAttribute;
          undefined testMethod(byte foo);
        };
     """
    )
    results = parser.finish()
    harness.check(
        len(results[1].members),
        6,
        "TestSecureContextOnInterfaceAfterPartialInterface should have six members",
    )
    harness.ok(
        results[1].getExtendedAttribute("SecureContext"),
        "Interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[1].members[0].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to constant members",
    )
    harness.ok(
        results[1].members[1].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to attribute members",
    )
    harness.ok(
        results[1].members[2].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from interface to method members",
    )
    harness.ok(
        results[1].members[3].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to constant members from "
            "partial interface"
        ),
    )
    harness.ok(
        results[1].members[4].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to attribute members from "
            "partial interface"
        ),
    )
    harness.ok(
        results[1].members[5].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to method members from partial "
            "interface"
        ),
    )

    parser = parser.reset()
    parser.parse(
        """
        interface TestSecureContextOnPartialInterface {
          const octet TEST_CONSTANT = 0;
          readonly attribute byte testAttribute;
          undefined testMethod(byte foo);
        };
        [SecureContext]
        partial interface TestSecureContextOnPartialInterface {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        6,
        "TestSecureContextOnPartialInterface should have six members",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext") is None,
        "[SecureContext] should not propagate from a partial interface to the interface",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial interface to the interface's "
            "constant members"
        ),
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial interface to the interface's "
            "attribute members"
        ),
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial interface to the interface's "
            "method members"
        ),
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext"),
        "Constant members from [SecureContext] partial interface should be [SecureContext]",
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        "Attribute members from [SecureContext] partial interface should be [SecureContext]",
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext"),
        "Method members from [SecureContext] partial interface should be [SecureContext]",
    )

    parser = parser.reset()
    parser.parse(
        """
        interface TestSecureContextOnInterfaceMembers {
          const octet TEST_NON_SECURE_CONSTANT_1 = 0;
          [SecureContext]
          const octet TEST_SECURE_CONSTANT       = 1;
          const octet TEST_NON_SECURE_CONSTANT_2 = 2;
          readonly attribute byte testNonSecureAttribute1;
          [SecureContext]
          readonly attribute byte testSecureAttribute;
          readonly attribute byte testNonSecureAttribute2;
          undefined testNonSecureMethod1(byte foo);
          [SecureContext]
          undefined testSecureMethod(byte foo);
          undefined testNonSecureMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        9,
        "TestSecureContextOnInterfaceMembers should have nine members",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext") is None,
        "[SecureContext] on members should not propagate up to the interface",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext") is None,
        "Constant should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext"),
        "Constant should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext") is None,
        "Constant should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext") is None,
        "Attribute should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        "Attribute should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext") is None,
        "Attribute should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[6].getExtendedAttribute("SecureContext") is None,
        "Method should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[7].getExtendedAttribute("SecureContext"),
        "Method should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[8].getExtendedAttribute("SecureContext") is None,
        "Method should not have [SecureContext] extended attribute",
    )

    parser = parser.reset()
    parser.parse(
        """
        interface TestSecureContextOnPartialInterfaceMembers {
        };
        partial interface TestSecureContextOnPartialInterfaceMembers {
          const octet TEST_NON_SECURE_CONSTANT_1 = 0;
          [SecureContext]
          const octet TEST_SECURE_CONSTANT       = 1;
          const octet TEST_NON_SECURE_CONSTANT_2 = 2;
          readonly attribute byte testNonSecureAttribute1;
          [SecureContext]
          readonly attribute byte testSecureAttribute;
          readonly attribute byte testNonSecureAttribute2;
          undefined testNonSecureMethod1(byte foo);
          [SecureContext]
          undefined testSecureMethod(byte foo);
          undefined testNonSecureMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        9,
        "TestSecureContextOnPartialInterfaceMembers should have nine members",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext") is None,
        "Constant from partial interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext"),
        "Constant from partial interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext") is None,
        "Constant from partial interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext") is None,
        "Attribute from partial interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        "Attribute from partial interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext") is None,
        "Attribute from partial interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[6].getExtendedAttribute("SecureContext") is None,
        "Method from partial interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[7].getExtendedAttribute("SecureContext"),
        "Method from partial interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[8].getExtendedAttribute("SecureContext") is None,
        "Method from partial interface should not have [SecureContext] extended attribute",
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            [SecureContext=something]
            interface TestSecureContextTakesNoValue1 {
              const octet TEST_SECURE_CONSTANT = 0;
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(threw, "[SecureContext] must take no arguments (testing on interface)")

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            interface TestSecureContextForOverloads1 {
              [SecureContext]
              undefined testSecureMethod(byte foo);
            };
            partial interface TestSecureContextForOverloads1 {
              undefined testSecureMethod(byte foo, byte bar);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        threw,
        (
            "If [SecureContext] appears on an overloaded operation, then it MUST appear on all "
            "overloads"
        ),
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            interface TestSecureContextForOverloads2 {
              [SecureContext]
              undefined testSecureMethod(byte foo);
            };
            partial interface TestSecureContextForOverloads2 {
              [SecureContext]
              undefined testSecureMethod(byte foo, byte bar);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        not threw,
        "[SecureContext] can appear on an overloaded operation if it appears on all overloads",
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            [SecureContext]
            interface TestSecureContextOnInterfaceAndMember {
              [SecureContext]
              undefined testSecureMethod(byte foo);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        threw, "[SecureContext] must not appear on an interface and interface member"
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            interface TestSecureContextOnPartialInterfaceAndMember {
            };
            [SecureContext]
            partial interface TestSecureContextOnPartialInterfaceAndMember {
              [SecureContext]
              undefined testSecureMethod(byte foo);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        threw,
        (
            "[SecureContext] must not appear on a partial interface and one of the partial "
            "interface's member's"
        ),
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            [SecureContext]
            interface TestSecureContextOnInterfaceAndPartialInterfaceMember {
            };
            partial interface TestSecureContextOnInterfaceAndPartialInterfaceMember {
              [SecureContext]
              undefined testSecureMethod(byte foo);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        threw,
        (
            "[SecureContext] must not appear on an interface and one of its partial interface's "
            "member's"
        ),
    )

    parser = parser.reset()
    threw = False
    try:
        parser.parse(
            """
            [SecureContext]
            interface TestSecureContextOnInheritedInterface {
            };
            interface TestSecureContextNotOnInheritingInterface : TestSecureContextOnInheritedInterface {
              undefined testSecureMethod(byte foo);
            };
        """
        )
        results = parser.finish()
    except WebIDL.WebIDLError:
        threw = True
    harness.ok(
        threw,
        (
            "[SecureContext] must appear on interfaces that inherit from another [SecureContext] "
            "interface"
        ),
    )

    # Test namespace
    parser = parser.reset()
    parser.parse(
        """
        [SecureContext]
        namespace TestSecureContextOnNamespace {
          const octet TEST_CONSTANT = 0;
          readonly attribute byte testAttribute;
          undefined testMethod(byte foo);
        };
        partial namespace TestSecureContextOnNamespace {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        6,
        "TestSecureContextOnNamespace should have six members",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext"),
        "Namespace should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from namespace to constant members",
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from namespace to attribute members",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from namespace to method members",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from namespace to "
            "constant members from partial namespace"
        ),
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from namespace to "
            "attribute members from partial namespace"
        ),
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext"),
        "[SecureContext] should propagate from namespace to method members from partial namespace",
    )

    parser = parser.reset()
    parser.parse(
        """
        namespace TestSecureContextOnNamespace {
          const octet TEST_CONSTANT = 0;
          readonly attribute byte testAttribute;
          undefined testMethod(byte foo);
        };
        [SecureContext]
        partial namespace TestSecureContextOnNamespace {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        6,
        "TestSecureContextOnNamespace should have six members",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext") is None,
        "Namespace should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial namespace to the namespace's "
            "constant members"
        ),
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial namespace to the namespace's "
            "attribute members"
        ),
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from a partial namespace to the namespace's "
            "method members"
        ),
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext"),
        "Constant members from [SecureContext] partial namespace should be [SecureContext]",
    )
    harness.ok(
        results[0].members[4].getExtendedAttribute("SecureContext"),
        "Attribute members from [SecureContext] partial namespace should be [SecureContext]",
    )
    harness.ok(
        results[0].members[5].getExtendedAttribute("SecureContext"),
        "Method members from [SecureContext] partial namespace should be [SecureContext]",
    )

    # Test 'includes'.
    parser = parser.reset()
    parser.parse(
        """
        [SecureContext]
        interface TestSecureContextInterfaceThatIncludesNonSecureContextMixin {
          const octet TEST_CONSTANT = 0;
        };
        interface mixin TestNonSecureContextMixin {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
        TestSecureContextInterfaceThatIncludesNonSecureContextMixin includes TestNonSecureContextMixin;
     """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        4,
        (
            "TestSecureContextInterfaceThatImplementsNonSecureContextInterface should have four "
            "members"
        ),
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext"),
        "Interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext"),
        (
            "[SecureContext] should propagate from interface to constant members even when other "
            "members are copied from a non-[SecureContext] interface"
        ),
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext") is None,
        "Constants copied from non-[SecureContext] mixin should not be [SecureContext]",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext") is None,
        "Attributes copied from non-[SecureContext] mixin should not be [SecureContext]",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext") is None,
        "Methods copied from non-[SecureContext] mixin should not be [SecureContext]",
    )

    parser = parser.reset()
    parser.parse(
        """
        interface TestSecureContextInterfaceThatIncludesNonSecureContextMixin {
          const octet TEST_CONSTANT = 0;
        };
        [SecureContext]
        interface mixin TestNonSecureContextMixin {
          const octet TEST_CONSTANT_2 = 0;
          readonly attribute byte testAttribute2;
          undefined testMethod2(byte foo);
        };
        TestSecureContextInterfaceThatIncludesNonSecureContextMixin includes TestNonSecureContextMixin;
     """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        4,
        (
            "TestSecureContextInterfaceThatImplementsNonSecureContextInterface should have four "
            "members"
        ),
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext") is None,
        "Interface should not have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext") is None,
        (
            "[SecureContext] should not propagate from interface to constant members when other "
            "members are copied from a [SecureContext] mixin"
        ),
    )
    harness.ok(
        results[0].members[1].getExtendedAttribute("SecureContext"),
        "Constants copied from [SecureContext] mixin should be [SecureContext]",
    )
    harness.ok(
        results[0].members[2].getExtendedAttribute("SecureContext"),
        "Attributes copied from [SecureContext] mixin should be [SecureContext]",
    )
    harness.ok(
        results[0].members[3].getExtendedAttribute("SecureContext"),
        "Methods copied from [SecureContext] mixin should be [SecureContext]",
    )

    # Test SecureContext and LegacyNoInterfaceObject
    parser = parser.reset()
    parser.parse(
        """
        [LegacyNoInterfaceObject, SecureContext]
        interface TestSecureContextLegacyNoInterfaceObject {
          undefined testSecureMethod(byte foo);
        };
    """
    )
    results = parser.finish()
    harness.check(
        len(results[0].members),
        1,
        "TestSecureContextLegacyNoInterfaceObject should have only one member",
    )
    harness.ok(
        results[0].getExtendedAttribute("SecureContext"),
        "Interface should have [SecureContext] extended attribute",
    )
    harness.ok(
        results[0].members[0].getExtendedAttribute("SecureContext"),
        "Interface member should have [SecureContext] extended attribute",
    )
