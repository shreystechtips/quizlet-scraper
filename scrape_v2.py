
from collections import defaultdict
import json as jsonify
# import re
import os
import time


def getTrueUrl(id, ending):
    url = "https://quizlet.com/" + str(id) + "/"
    # gets url for MC test
    return os.path.join(url, ending)


'''
PRE: Quizlet ID int (such as '3856167')
POST: Returns JSON for each question and its corresponding choices.
Choices will be repeated due to how quizlet works
override this by using the 'getFlashcardsJson' function
'''


def getMultipleChoiceJson(url, browser):
    if not url is str:
        browser.get(getTrueUrl(url, 'test'))

        # find and click button for options
        buttons = browser.find_elements_by_class_name("UIButton")
        for button in buttons:
            if button.text == "Options":
                button.click()

        # pattern = re.compile('[\w+]\s[\d]+\s\w+')
        num = "0"
        UIButtons = browser.find_elements_by_class_name(
            "TestModeOptions-questionLimitInputLabel")
        for thing in UIButtons:
            # pattern.match(thing.text)
            if "of" in thing.text and "questions" in thing.text:
                num = thing.text.split(" ")[1]
        print(num)
        browser.get(browser.current_url + '?questionCount=' +
                    num+'&questionTypes=4&showImages=true')

        # gets the question fields
        questions = browser.find_elements_by_class_name(
            "TestModeMultipleChoiceQuestion")
        json = defaultdict(dict)
        common = "div.TestModeMultipleChoiceQuestion-prompt.TestModeTermText.span."
        for values in questions:
            question = values.find_element_by_class_name(
                "TestModeTermText").text  # TestModeTermText
            choices = values.find_elements_by_class_name(
                "TestModeMultipleChoiceQuestion-choice")
            temp = []
            if not question or question.isspace():
                question = values.find_element_by_tag_name(
                    "img").get_attribute("src")
            for choice in choices:
                choice = choice.find_element_by_class_name(
                    "UIRadio-label").text  # TestModeTermText
                temp.append(choice)
            json[question] = temp
        return json
    else:
        raise ValueError('Input needs to be an integer, not a string')


def getFlashcardsJson(url, browser):
    browser.get(getTrueUrl(url, ""))
    blocks = browser.find_elements_by_class_name("SetPageTerm-contentWrapper")
    flashcards = browser.find_elements_by_class_name("SetPageTerm-wordText")
    answers = browser.find_elements_by_class_name("SetPageTerm-definitionText")
    iter = 0
    reps = 0
    cards = defaultdict(dict)
    for block in blocks:
        arr = []
        arr.append(answers[iter].text)
        test = None
        try:
            test = block.find_element_by_class_name(
                "leaflet-image-layer")
        except:
            test = None
        if not test == None:
            arr.append(test.get_attribute("src"))
        if flashcards[iter].text in cards:
            cards[flashcards[iter].text + ' number ' + str(reps)] = arr
            reps += 1
        else:
            cards[flashcards[iter].text] = arr
        iter += 1
    print(jsonify.dumps(cards))
    print(len(cards))
    print(iter)
    return cards


# print(getMultipleChoiceJson(385616707))
# print(getFlashcardsJson(385616707))
# time.sleep(15)
