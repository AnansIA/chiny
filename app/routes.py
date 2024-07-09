from flask import Flask, render_template, request, redirect, url_for
from .models import db, MeasuresMatrix, Matrix, Cavity, Piece, SHAPES
from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_matrix', methods=['GET', 'POST'])
def create_matrix():
    if request.method == 'POST':
        width_cm = request.form.get('width_cm')
        height_cm = request.form.get('height_cm')
        identifier = request.form.get('identifier')
        name = request.form.get('name')
        weight_unit_grs = request.form.get('weight_unit_grs')
        with_move = 'with_move' in request.form
        is_combinable = 'is_combinable' in request.form
        cavities_count = int(request.form.get('cavities'))

        measures_matrix = MeasuresMatrix(width_cm=width_cm, height_cm=height_cm)
        db.session.add(measures_matrix)
        db.session.commit()

        matrix = Matrix(
            identifier=identifier,
            measuresmatrix_id=measures_matrix.id,
            name=name,
            weight_unit_grs=weight_unit_grs,
            with_move=with_move,
            is_combinable=is_combinable
        )
        db.session.add(matrix)
        db.session.commit()

        for i in range(1, cavities_count + 1):
            piece_name = request.form.get(f'piece_name_{i}')
            piece_weight = request.form.get(f'piece_weight_{i}')
            piece_shape = request.form.get(f'piece_shape_{i}')

            piece = Piece(name=piece_name, weight_grs=piece_weight, shape=piece_shape)
            db.session.add(piece)
            db.session.commit()

            cavity_name = request.form.get(f'cavity_name_{i}')
            cavity = Cavity(
                matrix_id=matrix.id,
                name=cavity_name,
                piece_id=piece.id
            )
            db.session.add(cavity)
            db.session.commit()

        return redirect(url_for('create_matrix'))

    return render_template('create_matrix.html', shapes=SHAPES)
