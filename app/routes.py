from flask import Flask, render_template, request, redirect, url_for
from .models import db, MeasuresMatrix, Matrix, Cavity, Piece, Machine, SHAPES
from flask import current_app as app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_matrix', methods=['GET', 'POST'])
def create_matrix():
    if request.method == 'POST':
        width_mm = request.form.get('width_mm')
        height_mm = request.form.get('height_mm')
        identifier = request.form.get('identifier')
        name = request.form.get('name')
        weight_total_grs = request.form.get('weight_total_grs')
        with_move = 'with_move' in request.form
        is_combinable = 'is_combinable' in request.form
        cavities_count = int(request.form.get('cavities'))

        measures_matrix = MeasuresMatrix(width_mm=width_mm,
                                         height_mm=height_mm)
        db.session.add(measures_matrix)
        db.session.commit()

        matrix = Matrix(
            identifier=identifier,
            measuresmatrix_id=measures_matrix.id,
            name=name,
            with_move=with_move,
            weight_total_grs=weight_total_grs,
            is_combinable=is_combinable
        )
        db.session.add(matrix)
        db.session.commit()

        # Definir una sola pieza para todas las cavidades
        piece_name = request.form.get('piece_name')
        piece_weight = request.form.get('piece_weight')
        piece_shape = request.form.get('piece_shape')

        if piece_name and piece_weight and piece_shape:
            piece = Piece(name=piece_name,
                          weight_grs=piece_weight,
                          shape=piece_shape)
            db.session.add(piece)
            db.session.commit()

            for i in range(1, cavities_count + 1):
                cavity = Cavity(matrix_id=matrix.id, piece_id=piece.id)
                db.session.add(cavity)
                db.session.commit()
        else:
            for i in range(1, cavities_count + 1):
                piece_name = request.form.get(f'piece_name_{i}')
                piece_weight = request.form.get(f'piece_weight_{i}')
                piece_shape = request.form.get(f'piece_shape_{i}')

                if piece_name and piece_weight and piece_shape:
                    piece = Piece(name=piece_name,
                                  weight_grs=piece_weight,
                                  shape=piece_shape)
                    db.session.add(piece)
                    db.session.commit()

                    cavity = Cavity(matrix_id=matrix.id, piece_id=piece.id)
                    db.session.add(cavity)
                    db.session.commit()

        return redirect(url_for('create_matrix'))

    return render_template('create_matrix.html', shapes=SHAPES)


@app.route('/list_matrix')
def list_matrix():
    matrices = Matrix.query.all()
    matrices_data = []
    for matrix in matrices:
        measures_matrix = MeasuresMatrix.query.get(matrix.measuresmatrix_id)
        cavities = Cavity.query.filter_by(matrix_id=matrix.id).all()
        cavities_data = []
        for cavity in cavities:
            piece = Piece.query.get(cavity.piece_id)
            cavities_data.append({
                'piece_name': piece.name,
                'piece_weight': piece.weight_grs,
                'piece_shape': piece.shape
            })
        matrices_data.append({
            'identifier': matrix.identifier,
            'name': matrix.name,
            'with_move': matrix.with_move,
            'is_combinable': matrix.is_combinable,
            'weight_total_grs': matrix.weight_total_grs,
            'width_mm': measures_matrix.width_mm,
            'height_mm': measures_matrix.height_mm,
            'cavities': cavities_data
        })
    return render_template('list_matrix.html', matrices=matrices_data)


@app.route('/add_machine', methods=['GET', 'POST'])
def add_machine():
    if request.method == 'POST':
        brand_machine = request.form.get('brand_machine')
        ton = request.form.get('ton')
        has_close_cycle = 'has_close_cycle' in request.form
        has_injection_time = 'has_injection_time' in request.form
        has_curing_time = 'has_curing_time' in request.form
        has_waiting_time = 'has_waiting_time' in request.form

        machine = Machine(
            brand_machine=brand_machine,
            ton=ton,
            has_close_cycle=has_close_cycle,
            has_injection_time=has_injection_time,
            has_curing_time=has_curing_time,
            has_waiting_time=has_waiting_time
        )
        db.session.add(machine)
        db.session.commit()
        return redirect(url_for('list_machines'))
    return render_template('add_machine.html')
