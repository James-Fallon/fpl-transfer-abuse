import os


class Player:

    def __init__(self, name, photo_id, points):
        self.name = name
        self.photo_url = self._create_photo_url(photo_id)
        self.points = points

    @staticmethod
    def _create_photo_url(photo_id):
        pre, ext = os.path.splitext(photo_id)
        photo_png_file = pre + ".png"
        photo_url = "https://platform-static-files.s3.amazonaws.com/premierleague/photos/players/110x140/p" + photo_png_file
        return photo_url

    def get_details(self):
        return {
            'name': self.name,
            'points': self.points,
            'photo_url': self.photo_url
        }

    def __str__(self):
        return f'{self.name}: {self.points} points'

    def __repr__(self):
        return self.__str__()
