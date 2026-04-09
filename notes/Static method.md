You'll often encounter [[Method]]s that belong to a [[Class]], but don't need access to any [[Class variable]] or instance [[Attribute]]. As a result, they don't make sense as either [[Class method]] or [[Instance method]]. Instead, they usually provide utility services to the instance or [[Class method]]s, or to the users of the [[Class]]. These [[Method]]s are called **static methods**.

To define a static method, you use the `@staticmethod` [[Decorator]] followed by a [[Function definition]] that doesn't use a [[Self]] or [[Cls]] parameter. Example:
```python
class TheGame:
    # Game playing code goes here

    def play(self):
        pass

    @staticmethod
    def show_rules():
        print('These are the rules of the game')
        # The rules go here.

TheGame.show_rules()

game = TheGame()
game.play()
```
The only real difference between a [[Class method]] and a static method is that the static method doesn't have a [[Cls]] argument it can use.
