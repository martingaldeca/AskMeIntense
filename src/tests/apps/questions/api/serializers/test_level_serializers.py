from core.api.api_test_helpers import SerializerTestBase
from questions.api.serializers import LevelSerializer
from questions.factories import LevelFactory
from questions.models import Level


class LevelSerializerTestCase(SerializerTestBase):
    def test_data(self):
        level: Level = LevelFactory()
        expected_data = {
            "uuid": level.uuid.hex,
            "name": level.name,
            "description": level.description,
            "number": level.number,
        }
        self.assertEqual(LevelSerializer(level, context=self.context).data, expected_data)
