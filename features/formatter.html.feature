@sequential
Feature: HTML Formatter

    In order to export behave results
    As a tester
    I want that behave generates test run data in HTML format.


    @setup
    Scenario: Feature Setup
        Given a new working directory
        And a file named "features/steps/steps.py" with:
            """
            from behave import step

            @step('a step passes')
            def step_passes(context):
                pass

            @step('a step fails')
            def step_fails(context):
                assert False, "XFAIL-STEP"
            """

    Scenario: Use HTML formatter on feature without scenarios
        Given a file named "features/feature_without_scenarios.feature" with:
            """
            Feature: Simple, empty Feature
            """
        When I run "behave -f html features/feature_without_scenarios.feature"
        Then it should pass with:
            """
            0 features passed, 0 failed, 1 skipped
            0 scenarios passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: Simple, empty Feature</span>
              </h2>
            </div>
            """

    Scenario: Use HTML formatter on feature with description
        Given a file named "features/feature_with_description.feature" with:
            """
            Feature: Simple feature with description

                First feature description line.
                Second feature description line.

                Third feature description line (following an empty line).
            """
        When I run "behave -f html features/feature_with_description.feature"
        Then it should pass with:
            """
            0 features passed, 0 failed, 1 skipped
            0 scenarios passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: Simple feature with description</span>
              </h2>
              <pre class="message">First feature description line.
              Second feature description line.
              Third feature description line (following an empty line).</pre>
            </div>
            """

    Scenario: Use HTML formatter on feature with tags
        Given a file named "features/feature_with_tags.feature" with:
            """
            @foo @bar
            Feature: Simple feature with tags
            """
        When I run "behave -f html features/feature_with_tags.feature"
        Then it should pass with:
            """
            0 features passed, 0 failed, 1 skipped
            0 scenarios passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <span class="tag">@foo, @bar</span>
              <h2>
                <span class="val">Feature: Simple feature with tags</span>
              </h2>
            </div>
            """

    Scenario: Use HTML formatter on feature on one empty scenario
        Given a file named "features/feature_one_empty_scenario.feature" with:
            """
            Feature:
              Scenario: Simple scenario without steps
            """
        When I run "behave -f html features/feature_one_empty_scenario.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_empty_scenario.feature:2</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false">
                <span class="val">Scenario: Simple scenario without steps</span>
              </h3>
              <ol class="scenario_steps" id="scenario_0"/>
            </div>
            """

    Scenario: Use HTML formatter on feature on one empty scenario with description
        Given a file named "features/feature_one_empty_scenario_with_description.feature" with:
            """
            Feature:
              Scenario: Simple scenario with description but without steps
                First scenario description line.
                Second scenario description line.

                Third scenario description line (after an empty line).
            """
        When I run "behave -f html features/feature_one_empty_scenario_with_description.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_empty_scenario_with_description.feature:2</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false">
                <span class="val">Scenario: Simple scenario with description but without steps</span>
              </h3>
              <pre class="message">First scenario description line.
              Second scenario description line.
              Third scenario description line (after an empty line).</pre>
              <ol class="scenario_steps" id="scenario_0"/>
            </div>
            """

    Scenario: Use HTML formatter on feature on one empty scenario with tags
        Given a file named "features/feature_one_empty_scenario_with_tags.feature" with:
            """
            Feature:
              @foo @bar
              Scenario: Simple scenario with tags but without steps
            """
        When I run "behave -f html features/feature_one_empty_scenario_with_tags.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_empty_scenario_with_tags.feature:3</span>
              <span class="tag">@foo, @bar</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false">
                <span class="val">Scenario: Simple scenario with tags but without steps</span>
              </h3>
              <ol class="scenario_steps" id="scenario_0"/>
            </div>
            """

    Scenario: Use HTML formatter on feature on one passing scenario
        Given a file named "features/feature_one_passing_scenario.feature" with:
            """
            Feature:
              Scenario: Simple scenario with passing steps
                  Given a step passes
                  When a step passes
                  Then a step passes
                  And a step passes
                  But a step passes
            """
        When I run "behave -f html features/feature_one_passing_scenario.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_passing_scenario.feature:2</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false">
                <span class="val">Scenario: Simple scenario with passing steps</span>
              </h3>
              <ol class="scenario_steps" id="scenario_0">
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">Given </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">When </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">Then </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">And </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">But </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
              </ol>
            </div>
            """

    Scenario: Use HTML formatter on feature on one failing scenario
        Given a file named "features/feature_one_failing_scenario.feature" with:
            """
            Feature:
              Scenario: Simple scenario with failing step
                  Given a step passes
                  When a step passes
                  Then a step passes
                  And a step passes
                  But a step fails
            """
        When I run "behave -f html features/feature_one_failing_scenario.feature"
        Then it should fail with:
            """
            0 features passed, 1 failed, 0 skipped
            0 scenarios passed, 1 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_failing_scenario.feature:2</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false" style="background: #C40D0D; color: #FFFFFF">
                <span class="val">Scenario: Simple scenario with failing step</span>
              </h3>
              <ol class="scenario_steps" id="scenario_0">
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">Given </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">When </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">Then </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">And </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step failed"><div class="step_name"><span class="keyword">But </span><span class="step val">a step fails</span></div><div class="step_file"><span>features/steps/steps.py:7</span></div><span class="embed"/><a class="message" onclick="rslt=document.getElementById('embed_1');rslt.style.display =(rslt.style.display == 'none' ? 'block' : 'none');return false">Error message</a><pre id="embed_1" style="display: none; white-space: pre-wrap;">Assertion Failed: XFAIL-STEP</pre>    </li>
              </ol>
            </div>
            """

    Scenario: Use HTML formatter on feature with one scenario with skipped steps
        Given a file named "features/feature_one_failing_scenario_with_skipped_steps.feature" with:
            """
            Feature:
              Scenario: Simple scenario with failing and skipped steps
                  Given a step passes
                  When a step fails
                  Then a step passes
                  And a step passes
                  But a step passes
            """
        When I run "behave -f html features/feature_one_failing_scenario_with_skipped_steps.feature"
        Then it should fail with:
            """
            0 features passed, 1 failed, 0 skipped
            0 scenarios passed, 1 failed, 0 skipped
            """
        And the command output should contain:
            """
            <div class="feature">
              <h2>
                <span class="val">Feature: </span>
              </h2>
            </div>
            <div class="scenario">
              <span class="scenario_file">features/feature_one_failing_scenario_with_skipped_steps.feature:2</span>
              <h3 onclick="ol=document.getElementById('scenario_0');ol.style.display =(ol.style.display == 'none' ? 'block' : 'none');return false" style="background: #C40D0D; color: #FFFFFF">
                <span class="val">Scenario: Simple scenario with failing and skipped steps</span>
              </h3>
              <ol class="scenario_steps" id="scenario_0">
                <li class="step passed">
                  <div class="step_name">
                    <span class="keyword">Given </span>
                    <span class="step val">a step passes</span>
                  </div>
                  <div class="step_file">
                    <span>features/steps/steps.py:3</span>
                  </div>
                  <span class="embed"/>
                </li>
                <li class="step failed"><div class="step_name"><span class="keyword">When </span><span class="step val">a step fails</span></div><div class="step_file"><span>features/steps/steps.py:7</span></div><span class="embed"/><a class="message" onclick="rslt=document.getElementById('embed_1');rslt.style.display =(rslt.style.display == 'none' ? 'block' : 'none');return false">Error message</a><pre id="embed_1" style="display: none; white-space: pre-wrap;">Assertion Failed: XFAIL-STEP</pre>    </li>
              </ol>
            </div>
            """
