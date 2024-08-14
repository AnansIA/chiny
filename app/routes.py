from flask import Flask, render_template, request, redirect, url_for, jsonify
from .models import db, MeasuresMatrix, Matrix, Cavity, Piece, Machine, Person, SHAPES, Holder, MatrixHolderAssociation, Order
from flask import current_app as app
from datetime import datetime


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
        type_matrix = int(request.form.get('type_matrix'))  # Nuevo campo
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
            is_combinable=is_combinable,
            type_matrix=type_matrix
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

        return redirect(url_for('list_matrix'))

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
            'id': matrix.id,
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

@app.route('/list_holders')
def list_holders():
    holders = Holder.query.all()
    return render_template('list_holders.html', holders=holders)

@app.route('/list_persons')
def list_persons():
    persons = Person.query.all()
    return render_template('list_persons.html', persons=persons)


@app.route('/list_associations')
def list_associations():
    associations = MatrixHolderAssociation.query.all()
    return render_template('list_associations.html', associations=associations)

@app.route('/list_machines')
def list_machines():
    machines = Machine.query.all()
    return render_template('list_machines.html', machines=machines)

@app.route('/list_orders')
def list_orders():
    orders = Order.query.all()
    return render_template('list_orders.html', orders=orders)

@app.route('/list_productions')
def list_productions():
    productions = Production.query.all()
    return render_template('list_productions.html', productions=productions)

@app.route('/create_person', methods=['POST'])
def create_person():
    fullname = request.form.get('fullname')
    observ = request.form.get('observ')

    if fullname:
        person = Person(fullname=fullname, observ=observ)
        db.session.add(person)
        db.session.commit()
        return jsonify({'message': 'Person created successfully'}), 201
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/create_holder', methods=['GET', 'POST'])
def create_holder():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        width_cm = request.form.get('width_cm')
        height_cm = request.form.get('height_cm')
        max_weight_grs = request.form.get('max_weight_grs')
        num_spaces = request.form.get('num_spaces')
        with_move = 'with_move' in request.form

        holder = Holder(
            identifier=identifier,
            width_cm=width_cm,
            height_cm=height_cm,
            max_weight_grs=max_weight_grs,
            num_spaces=num_spaces,
            with_move=with_move,
            available=True  # Se crea disponible por defecto
        )
        db.session.add(holder)
        db.session.commit()

        return redirect(url_for('list_holders'))

    return render_template('create_holder.html')

@app.route('/edit_matrix/<int:matrix_id>', methods=['GET', 'POST'])
def edit_matrix(matrix_id):
    matrix = Matrix.query.get_or_404(matrix_id)
    if request.method == 'POST':
        matrix.identifier = request.form.get('identifier')
        matrix.name = request.form.get('name')
        matrix.weight_total_grs = request.form.get('weight_total_grs')
        matrix.with_move = 'with_move' in request.form
        matrix.is_combinable = 'is_combinable' in request.form
        matrix.type_matrix = int(request.form.get('type_matrix'))  # Nuevo campo
        db.session.commit()

        return redirect(url_for('list_matrix'))

    return render_template('edit_matrix.html', matrix=matrix)


# Ruta para editar portamoldes
@app.route('/edit_holder/<int:holder_id>', methods=['GET', 'POST'])
def edit_holder(holder_id):
    holder = Holder.query.get_or_404(holder_id)
    if request.method == 'POST':
        holder.identifier = request.form.get('identifier')
        holder.width_cm = request.form.get('width_cm')
        holder.height_cm = request.form.get('height_cm')
        holder.max_weight_grs = request.form.get('max_weight_grs')
        holder.num_spaces = request.form.get('num_spaces')
        holder.with_move = 'with_move' in request.form
        db.session.commit()
        return redirect(url_for('list_holders'))
    return render_template('edit_holder.html', holder=holder)


@app.route('/create_association', methods=['GET', 'POST'])
def create_association():
    if request.method == 'POST':
        matrix_id = request.form.get('matrix_id')
        holder_id = request.form.get('holder_id')

        # Crear la asociación
        association = MatrixHolderAssociation(matrix_id=matrix_id, holder_id=holder_id)
        db.session.add(association)

        # Marcar la matriz y el portamolde como no disponibles
        matrix = Matrix.query.get(matrix_id)
        holder = Holder.query.get(holder_id)
        matrix.is_available = False
        holder.available = False  # Usar el campo existente

        db.session.commit()

        return redirect(url_for('list_associations'))

    matrices = Matrix.query.filter_by(is_available=True).all()
    holders = Holder.query.filter_by(available=True).all()  # Usar el campo existente
    return render_template('create_association.html', matrices=matrices, holders=holders)


@app.route('/disarm_association/<int:association_id>', methods=['POST'])
def disarm_association(association_id):
    association = MatrixHolderAssociation.query.get_or_404(association_id)

    # Marcar la matriz y el portamolde como disponibles
    matrix = Matrix.query.get(association.matrix_id)
    holder = Holder.query.get(association.holder_id)
    matrix.is_available = True
    holder.available = True

    # Eliminar la asociación
    db.session.delete(association)
    db.session.commit()

    return redirect(url_for('list_associations'))


@app.route('/create_machine', methods=['GET', 'POST'])
def create_machine():
    if request.method == 'POST':
        name = request.form.get('name')
        brand_machine = request.form.get('brand_machine')
        ton = request.form.get('ton')
        has_close_cycle = 'has_close_cycle' in request.form
        has_injection_time = 'has_injection_time' in request.form
        has_curing_time = 'has_curing_time' in request.form
        has_waiting_time = 'has_waiting_time' in request.form

        machine = Machine(
            name=name,
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

    return render_template('create_machine.html')


@app.route('/edit_machine/<int:machine_id>', methods=['GET', 'POST'])
def edit_machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    if request.method == 'POST':
        machine.name = request.form.get('name')
        machine.brand_machine = request.form.get('brand_machine')
        machine.ton = request.form.get('ton')
        machine.has_close_cycle = 'has_close_cycle' in request.form
        machine.has_injection_time = 'has_injection_time' in request.form
        machine.has_curing_time = 'has_curing_time' in request.form
        machine.has_waiting_time = 'has_waiting_time' in request.form

        db.session.commit()
        return redirect(url_for('list_machines'))

    return render_template('edit_machine.html', machine=machine)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        product = request.form.get('product')
        quantity = request.form.get('quantity')
        client = request.form.get('client')
        delivery_date_str = request.form.get('delivery_date')
        delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()  # Convertir a objeto date
        priority = request.form.get('priority')
        matrix_identifier = request.form.get('matrix_identifier')
        observation = request.form.get('observation')

        order = Order(
            product=product,
            quantity=quantity,
            client=client,
            delivery_date=delivery_date,
            priority=priority,
            matrix_identifier=matrix_identifier,
            observation=observation
        )
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('list_orders'))

    matrices = Matrix.query.all()
    return render_template('create_order.html', matrices=matrices)


@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        order.product = request.form.get('product')
        order.quantity = request.form.get('quantity')
        order.client = request.form.get('client')
        delivery_date_str = request.form.get('delivery_date')
        order.delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        order.priority = request.form.get('priority')
        order.matrix_identifier = request.form.get('matrix_identifier')
        order.observation = request.form.get('observation')

        db.session.commit()
        return redirect(url_for('list_orders'))

    matrices = Matrix.query.all()

@app.route('/create_production', methods=['GET', 'POST'])
def create_production():
    if request.method == 'POST':
        order_ids = request.form.getlist('order_ids')
        matrix_id = request.form.get('matrix_id')
        holder_id = request.form.get('holder_id')
        machine_id = request.form.get('machine_id')
        person_id = request.form.get('person_id')
        action = request.form.get('action')
        injection_qty = int(request.form.get('injection_qty'))

        matrix = Matrix.query.get(matrix_id)
        active_cavities = matrix.cavities_count  # Obtén el número de cavidades activas desde la configuración de la matriz
        piece_weight_grs = matrix.piece_weight_grs  # Obtén el peso de la pieza desde la configuración de la matriz

        total_pieces = injection_qty * active_cavities
        total_weight_kilos = (total_pieces * piece_weight_grs) / 1000  # Convertir a kilos

        identifier = f"{datetime.now().strftime('%Y%m%d')}-{order_ids[0]}"  # Usamos el primer pedido como referencia para el identificador

        production = Production(
            matrix_id=matrix_id,
            holder_id=holder_id,
            machine_id=machine_id,
            person_id=person_id,
            action=action,
            injection_qty=injection_qty,
            action_time=datetime.utcnow(),
            total_pieces=total_pieces,
            total_weight_kilos=total_weight_kilos,
            identifier=identifier,
            production_date=datetime.utcnow().date()
        )
        db.session.add(production)
        db.session.commit()

        for order_id in order_ids:
            production_order = ProductionOrder(
                production_id=production.id,
                order_id=order_id
            )
            db.session.add(production_order)
        
        db.session.commit()

        return redirect(url_for('list_productions'))

    orders = Order.query.all()
    matrices = Matrix.query.all()
    holders = Holder.query.all()
    machines = Machine.query.all()
    persons = Person.query.all()

    return render_template('create_production.html', orders=orders, matrices=matrices, holders=holders, machines=machines, persons=persons)

@app.route('/edit_holder_matrices/<int:holder_id>', methods=['GET', 'POST'])
def edit_holder_matrices(holder_id):
    holder = Holder.query.get_or_404(holder_id)

    if request.method == 'POST':
        matrix_id = request.form.get('matrix_id')
        existing_association = MatrixHolderAssociation.query.filter_by(matrix_id=matrix_id, holder_id=holder_id).first()

        if existing_association:
            existing_association.is_active = True
        else:
            new_association = MatrixHolderAssociation(matrix_id=matrix_id, holder_id=holder_id)
            db.session.add(new_association)

        db.session.commit()
        return redirect(url_for('edit_holder_matrices', holder_id=holder_id))

    available_matrices = Matrix.query.filter(~Matrix.associations.any(holder_id=holder_id)).all()
    return render_template('edit_holder_matrices.html', holder=holder, available_matrices=available_matrices)

@app.route('/remove_matrix_from_holder/<int:association_id>', methods=['POST'])
def remove_matrix_from_holder(association_id):
    association = MatrixHolderAssociation.query.get_or_404(association_id)
    association.is_active = False
    db.session.commit()
    return redirect(url_for('edit_holder_matrices', holder_id=association.holder_id))


@app.route('/reactivate_matrix_in_holder/<int:association_id>', methods=['POST'])
def reactivate_matrix_in_holder(association_id):
    association = MatrixHolderAssociation.query.get_or_404(association_id)
    association.is_active = True
    db.session.commit()
    return redirect(url_for('edit_holder_matrices', holder_id=association.holder_id))

