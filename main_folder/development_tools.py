class Trigger:
    def __init__(self, collider, function, pass_value=False):
        self.collider = collider
        self.function = function
        self.pass_value = pass_value

    def collide(self, box_collider):
        return self.collider.colliderect(box_collider)

    def trig(self, value):
        if self.pass_value:
            self.function(value)
        else:
            self.function()
