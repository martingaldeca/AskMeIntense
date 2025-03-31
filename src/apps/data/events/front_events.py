from data.events import FrontendDataEvent


class PageChangeEvent(FrontendDataEvent):
    event_type = "page_change"
    description = "This event is triggered when page in the frontend changes."


class StartGameFirstClickEvent(FrontendDataEvent):
    event_type = "start_game_first"
    description = "This event is triggered when any user clicks on start game button."


class StartGameAfterSelectedCategoryAndLevelClickEvent(FrontendDataEvent):
    event_type = "start_game_after_selected_category_and_level"
    description = "This event is triggered when any user clicks on start game button after selected category and level."


class LevelSelectedEvent(FrontendDataEvent):
    event_type = "level_selected"
    description = (
        "This event is triggered when any user select a level in the selectors."
    )


class CategorySelectedEvent(FrontendDataEvent):
    event_type = "category_selected"
    description = (
        "This event is triggered when any user select a category in the selectors."
    )


class QuestionDetailDisplayedEvent(FrontendDataEvent):
    event_type = "question_detail_displayed"
    description = (
        "This event is triggered when a question detail is displayed in the frontend."
    )


class NextRandomQuestionClickEvent(FrontendDataEvent):
    event_type = "next_random_question"
    description = "This event is triggered when a next random question is clicked."



class NavigatorHomeClickEvent(FrontendDataEvent):
    event_type = "navigator_home_click"
    description = "This event is triggered when a navigator home button is clicked."


class NavigatorFavoritesClickEvent(FrontendDataEvent):
    event_type = "navigator_favorites_click"
    description = "This event is triggered when a navigator favorites button is clicked."


class NavigatorProfileClickEvent(FrontendDataEvent):
    event_type = "navigator_profile_click"
    description = "This event is triggered when a navigator profile button is clicked."


class NavigatorLoginClickEvent(FrontendDataEvent):
    event_type = "navigator_profile_click"
    description = "This event is triggered when a navigator profile button is clicked."
