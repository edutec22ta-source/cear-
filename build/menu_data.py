# Cardápio real do Restaurante Ceará Grill, transcrito dos flyers enviados (02/10/2026).
# Cada item: (nome, descrição ou None, [opções])
# Opção: (rótulo visível ou None, preço, nome que vai para o pedido ou None = nome do item)

ACOMP_FAROFA = "Acompanha arroz, feijão, farofa, fritas e salada."
ACOMP_OVO = "Acompanha arroz, feijão, ovo, fritas e salada."
ACOMP = "Acompanha arroz, feijão, fritas e salada."

CATEGORIAS = [
    {
        "id": "pratos",
        "titulo": "Pratos especiais",
        "itens": [
            ("Picanha", ACOMP_FAROFA, [(None, 47, None)]),
            ("Churrasco ou asinha de frango assada", ACOMP_FAROFA, [
                ("Churrasco", 37, "Churrasco"),
                ("Asinha", 37, "Asinha de frango assada"),
            ]),
            ("Costelinha assada, frango assado, linguiça assada e calabresa", ACOMP_FAROFA, [
                ("Médio", 25, None),
                ("Grande", 27, None),
            ]),
            ("Filé de frango", ACOMP_FAROFA, [("Médio", 25, None), ("Grande", 27, None)]),
            ("Filé de frango à cavalo", ACOMP_OVO, [(None, 35, None)]),
            ("Filé de frango à parmegiana", ACOMP, [(None, 42, None)]),
            ("Contra filé", ACOMP, [(None, 38, None)]),
            ("Contra filé à cavalo", ACOMP_OVO, [(None, 40, None)]),
            ("Contra filé à parmegiana", ACOMP, [(None, 44, None)]),
            ("Omelete", ACOMP, [(None, 34, None)]),
            ("Filé de merluza", ACOMP, [(None, 34, None)]),
            ("Filé de tilápia", ACOMP, [(None, 41, None)]),
        ],
    },
    {
        "id": "marmitas",
        "titulo": "Marmitas do dia",
        "itens": [
            ("Marmita de churrasco só carne", "Acompanha arroz, feijão, farofa, fritas e salada verde.", [(None, 38, None)]),
            ("Rabada", "Acompanha arroz, feijão, polenta ou macarrão e salada verde.", [(None, 35, None)]),
            ("Picadinho", "Acompanha arroz, feijão, macarrão e salada verde.", [("Média", 25, None), ("Grande", 27, None)]),
            ("Dobradinha", "Acompanha arroz, farofa e salada verde.", [("Média", 25, None), ("Grande", 27, None)]),
            ("Filé de peixe panga frito", "Acompanha arroz, feijão, fritas ou purê e salada verde.", [(None, 35, None)]),
        ],
    },
    {
        "id": "cafe",
        "titulo": "Café da manhã",
        "itens": [
            ("Misto quente", "Pão, presunto e queijo.", [(None, 14, None)]),
            ("Misto frio", "Pão, presunto e queijo.", [(None, 12, None)]),
            ("Bauru", "Pão, presunto, queijo e tomate.", [(None, 14, None)]),
            ("Sanduíche de filé de frango", "Pão, filé de frango, alface, tomate e maionese.", [(None, 21, None)]),
            ("Sanduíche de contra filé", "Pão, contra filé, queijo, alface e tomate.", [(None, 27, None)]),
            ("Cuscuz com queijo", None, [(None, 18, None)]),
            ("Cuscuz com calabresa", None, [(None, 18, None)]),
            ("Cuscuz com ovo", None, [(None, 18, None)]),
        ],
        "salgados": {
            "preco": 5,
            "nomes": ["Pão de queijo", "Coxinha", "Risole", "Bolinha de carne", "Enroladinho de salsicha"],
        },
    },
]
