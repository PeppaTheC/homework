from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        raise NotImplemented


class Observable(ABC):
    def __init__(self) -> None:
        self.observers = []

    def subscribe(self, observer: Observer) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)


class MyTubeUser(Observer):
    def __init__(self, user_name: str):
        self._name = user_name

    def update(self, message: str):
        print(f"Dear {self._name}, {message}")


class MyTubeChannel(Observable):
    def __init__(self, channel_name: str, channel_owner: MyTubeUser):
        super().__init__()
        self.name = channel_name
        self.owner = channel_owner
        self.playlists = {}

    def subscribe(self, user: MyTubeUser):
        super().subscribe(user)

    def publish_video(self, video: str):
        self.notify_observers(f"There is new video on \'{self.name}\' channel: \'{video}\'")

    def publish_playlist(self, name: str, playlist: list):
        self.playlists[name] = playlist
        self.notify_observers(f"There is new playlist on \'{self.name}\' channel: \'{name}\'")


if __name__ == '__main__':
    matt = MyTubeUser('Matt')
    john = MyTubeUser('John')
    erica = MyTubeUser('Erica')

    dogs_life = MyTubeChannel('All about dogs', matt)
    dogs_life.subscribe(john)
    dogs_life.subscribe(erica)

    dogs_nutrition_videos = ['What do dogs eat?', 'Which Pedigree pack to choose?']
    dogs_nutrition_playlist = {'Dogs nutrition': dogs_nutrition_videos}

    for video in dogs_nutrition_videos:
        dogs_life.publish_video(video)

    dogs_life.publish_playlist('Dogs nutrition', dogs_nutrition_videos)
