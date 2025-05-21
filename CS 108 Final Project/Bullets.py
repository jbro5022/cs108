
class Bullets:
    """ Particle models a single particle that may be rendered to a canvas. """

    def __init__(self, x=50, y=50, vel_x=0, vel_y=-10, radius=40, color="red", up=1):
        """Instantiate a particle object."""
        self.x = x
        self.y = y - 65
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color
        self.up = up

    # Add your methods here.
    def move(self, drawing):
        if self.x + self.radius > drawing.width or self.x - self.radius < 0:
            self.vel_x *= -1
        self.x += self.vel_x 
        self.y += self.vel_y
        
    def draw(self, drawing):
        drawing.rectangle(self.x - 5 , self.y, 
             self.x + 5,
             self.y + 20,
            color=self.color
             )
    
        
    def hits(self, other):
        """ Determine if I've collided with 'other'. """
        if self == other:
            # I can't collide with myself.
            return False

        # Determine if I overlap with the other particle.
        return (
                self.radius + other.radius >=
                distance(self.x, self.y, other.x, other.y)
        )

    def bounce(self, other):
        """Handle elastic collisions between this particle and 'other'.

        This method checks if the two particles collide and, if so, modifies
        the positions and velocities to reflect the result of the collision.

        The result is reasonably physically accurate, but limited by being
        run only *after* a collision has already occurred.

        Both objects are changed, so this method should only be run once for each pair of objects.

        Thanks to Dr. Paul Harper (Calvin Physics).
        """
        if not self.hits(other):
            return

        # Calculate masses (proportional to area)
        m1 = self.radius ** 2
        m2 = other.radius ** 2
        m1_m2 = m1 + m2

        # Calculate new velocities. See the "angle-free representation" at
        # https://en.m.wikipedia.org/wiki/Elastic_collision
        dx = self.x - other.x
        dy = self.y - other.y
        dist_squared = dx * dx + dy * dy
        dvx = self.vel_x - other.vel_x
        dvy = self.vel_y - other.vel_y

        dot_product_2 = 2 * (dvx * dx + dvy * dy) / dist_squared
        dv1_scale = m2 / m1_m2 * dot_product_2
        dv2_scale = m1 / m1_m2 * dot_product_2

        self.vel_x -= dv1_scale * dx
        self.vel_y -= dv1_scale * dy
        other.vel_x += dv2_scale * dx
        other.vel_y += dv2_scale * dy

        # Fix up the positions to ensure they're not stuck together.
        dist = dist_squared ** 0.5
        dist_x_norm = dx / dist
        dist_y_norm = dy / dist
        intrusion_distance = (self.radius + other.radius - dist) / 2 + 1e-6

        self.x += intrusion_distance * dist_x_norm
        self.y += intrusion_distance * dist_y_norm
        other.x -= intrusion_distance * dist_x_norm
        other.y -= intrusion_distance * dist_y_norm