class ResourceTestData:
    @property
    def existing_resource(self):
        return {
            "title": "sample title",
            "content": "sample content",
        }

    @property
    def create_resource(self):
        return {
            "title": "new title",
            "content": "new content",
        }

    @property
    def update_resource(self):
        return {
            "title": "update title"
        }
