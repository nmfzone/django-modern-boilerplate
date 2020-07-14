Feature: Login

    Scenario: Logging in
        Given user "johndoe" exists
        When a web browser is on the Login page
        Then I fill in "username" with "johndoe"
        Then I fill in "password" with "12345678"
        Then I press ".submit-btn"
        Then I should be on "/dashboard"
