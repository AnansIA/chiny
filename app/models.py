from . import db

SHAPES = [
    'Circular', 'Rectangular', 'Square', 'Oval', 'Triangular', 'Hexagonal',
    'Octagonal', 'Elliptical', 'Cylindrical', 'Conical', 'Spherical',
    'Cuboidal', 'Tetrahedral', 'Pyramidal', 'Trapezoidal', 'Parallelogram',
    'Rhomboidal', 'Star-shaped', 'Heart-shaped', 'Crescent', 'Semi-circular',
    'Polygonal', 'Irregular', 'Custom'
]


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
    identifier = db.Column(db.String(5), nullable=False)
    measuresmatrix_id = db.Column(db.Integer,
                                  db.ForeignKey('measuresmatrix.id'),
                                  nullable=False)
    name = db.Column(db.String(120), nullable=False)
    weight_unit_grs = db.Column(db.Float, nullable=False)
    with_move = db.Column(db.Boolean, default=False)
    is_combinable = db.Column(db.Boolean, default=True)
    cavities = db.relationship('Cavity', backref='matrix', lazy=True)


class Cavity(db.Model):
    __tablename__ = 'cavity'
    id = db.Column(db.Integer, primary_key=True)
    matrix_id = db.Column(db.Integer,
                          db.ForeignKey('matrix.id'),
                          nullable=False)
    name = db.Column(db.String(120), nullable=False)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('piece.id'),
                         nullable=False)


class Holder(db.Model):
    __tablename__ = 'holder'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(5), nullable=False)
    width_cm = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Integer, nullable=False)
    weight_grs = db.Column(db.Float, default=0)
    with_move = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)


class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key=True)
    brand_machine = db.Column(db.String(120), nullable=False)
    ton = db.Column(db.Integer, nullable=False)
