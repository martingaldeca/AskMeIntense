from .base import (
    BackendDataEvent,
    DataEvent,
    FrontendDataEvent,
    RsyncUserPropertiesEvent,
)
from .front_events import (
    StartGameFirstClickEvent,
    PageChangeEvent,
    LevelSelectedEvent,
    CategorySelectedEvent,
    StartGameAfterSelectedCategoryAndLevelClickEvent,
    QuestionDetailDisplayedEvent,
    NextRandomQuestionClickEvent,
    NavigatorHomeClickEvent,
    NavigatorFavoritesClickEvent,
    NavigatorProfileClickEvent,
    NavigatorLoginClickEvent,
)

# Document events
events = {
    DataEvent.event_type: DataEvent,
    RsyncUserPropertiesEvent.event_type: RsyncUserPropertiesEvent,
    # Front events
    PageChangeEvent.event_type: PageChangeEvent,
    StartGameFirstClickEvent.event_type: StartGameFirstClickEvent,
    StartGameAfterSelectedCategoryAndLevelClickEvent.event_type: StartGameAfterSelectedCategoryAndLevelClickEvent,
    LevelSelectedEvent.event_type: LevelSelectedEvent,
    CategorySelectedEvent.event_type: CategorySelectedEvent,
    QuestionDetailDisplayedEvent.event_type: QuestionDetailDisplayedEvent,
    NextRandomQuestionClickEvent.event_type: NextRandomQuestionClickEvent,
    NavigatorHomeClickEvent.event_type: NavigatorHomeClickEvent,
    NavigatorFavoritesClickEvent.event_type: NavigatorFavoritesClickEvent,
    NavigatorProfileClickEvent.event_type: NavigatorProfileClickEvent,
    NavigatorLoginClickEvent.event_type: NavigatorLoginClickEvent,
}
