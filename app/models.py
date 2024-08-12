from . import db

SHAPES = [
    'Circular', 'Rectangular', 'Square', 'Oval', 'Triangular', 'Hexagonal',
    'Octagonal', 'Elliptical', 'Cylindrical', 'Conical', 'Spherical',
    'Cuboidal', 'Tetrahedral', 'Pyramidal', 'Trapezoidal', 'Parallelogram',
    'Rhomboidal', 'Star-shaped', 'Heart-shaped', 'Crescent', 'Semi-circular',
    'Polygonal', 'Irregular', 'Custom'
]

# Matrix and Holders
# ------------------


class Piece(db.Model):
    __tablename__ = 'piece'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    weight_grs = db.Column(db.Float, nullable=False)
    shape = db.Column(db.String(50), nullable=False)
    cavities = db.relationship('Cavity', backref='piece', lazy=True)

    def __init__(self, name, weight_grs, shape):
        self.name = name
        self.weight_grs = weight_grs
        if shape not in SHAPES:
            raise ValueError(f"the shape {shape} is invalid.")
        self.shape = shape


class MeasuresMatrix(db.Model):
    __tablename__ = 'measuresmatrix'
    id = db.Column(db.Integer, primary_key=True)
    width_mm = db.Column(db.Integer, nullable=False)
    height_mm = db.Column(db.Integer, nullable=False)
    matrices = db.relationship('Matrix', backref='measuresmatrix', lazy=True)

class Matrix(db.Model):
    __tablename__ = 'matrix'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(5), nullable=False, unique=True)
    measuresmatrix_id = db.Column(db.Integer, db.ForeignKey('measuresmatrix.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    weight_total_grs = db.Column(db.Float, nullable=False)
    with_move = db.Column(db.Boolean, default=False)
    is_combinable = db.Column(db.Boolean, default=True)
    type_matrix = db.Column(db.Integer, nullable=False, default=4)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=True)  # Clave foránea que apunta a Sector
    cavities = db.relationship('Cavity', backref='matrix', lazy=True)
    is_available = db.Column(db.Boolean, default=True)


class Cavity(db.Model):
    __tablename__ = 'cavity'
    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer,
                          db.ForeignKey('matrix.id'),
                          nullable=False)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('piece.id'),
                         nullable=False)


class Holder(db.Model):
    __tablename__ = 'holder'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(5), nullable=False)
    width_cm = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Integer, nullable=False)
    max_weight_grs = db.Column(db.Float, nullable=False)
    with_move = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)
    num_spaces = db.Column(db.Integer, nullable=False)  # Número de espacios
    sectors = db.relationship('Sector', backref='holder', lazy=True)

class Sector(db.Model):
    __tablename__ = 'sector'
    id = db.Column(db.Integer, primary_key=True)
    holder_id = db.Column(db.Integer, db.ForeignKey('holder.id'), nullable=False)
    position = db.Column(db.String(50), nullable=False)  # Ejemplo: "Izquierda", "Derecha", "Centro"
    allows_move = db.Column(db.Boolean, default=False)
    max_matrices = db.Column(db.Integer, nullable=False)
    matrices = db.relationship('Matrix', backref='sector', lazy=True)


# Var Variables
# --------------

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    observ = db.Column(db.String(250))

# Orders
# -------

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    client = db.Column(db.String(120), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(10), nullable=False, default='Normal')  # Puede ser 'High', 'Normal', o 'Low'
    matrix_identifier = db.Column(db.String(5), db.ForeignKey('matrix.identifier'), nullable=False)
    observation = db.Column(db.String(255), nullable=True)

    matrix = db.relationship('Matrix', backref='orders')

# Machines
# --------


class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    brand_machine = db.Column(db.String(119), nullable=False)
    ton = db.Column(db.Integer, nullable=False)
    has_close_cycle = db.Column(db.Boolean, default=False)
    has_injection_time = db.Column(db.Boolean, default=False)
    has_curing_time = db.Column(db.Boolean, default=False)
    has_waiting_time = db.Column(db.Boolean, default=False)
    productions = db.relationship('Production', backref='machine', lazy=True)


# Actions
# -------

class Production(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    holder_id = db.Column(db.Integer,
                          db.ForeignKey('holder.id'),
                          nullable=False)
    machine_id = db.Column(db.Integer,
                           db.ForeignKey('machine.id'),
                           nullable=False)
    person_id = db.Column(db.Integer,
                          db.ForeignKey('person.id'),
                          nullable=False)
    close_cycle = db.Column(db.Float, nullable=True)
    injection_time = db.Column(db.Float, nullable=True)
    curing_time = db.Column(db.Float, nullable=True)
    waiting_time = db.Column(db.Float, nullable=True)
    production_date = db.Column(db.Date, nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=True)


class MatrixHolderAssociation(db.Model):
    __tablename__ = 'matrix_holder_association'
    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'), nullable=False)
    holder_id = db.Column(db.Integer, db.ForeignKey('holder.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Indica si la asociación está activa
    
    matrix = db.relationship('Matrix', backref=db.backref('associations', cascade="all, delete-orphan"))
    holder = db.relationship('Holder', backref=db.backref('associations', cascade="all, delete-orphan"))
