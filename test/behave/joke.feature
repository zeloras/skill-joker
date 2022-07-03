Feature: mycroft-joker

  Scenario Outline: Make screenshot
    Given an english speaking user
     When the user says "<make a shot>"
     Then "mycroft-joker" should reply status

  Examples: request a screenshot
    | do a shoot |
    | make screenshot |
    | shot it |


