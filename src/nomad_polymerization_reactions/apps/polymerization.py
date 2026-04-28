from nomad.config.models.ui import (
    App,
    Axis,
    AxisQuantity,
    BreakpointEnum,
    Column,
    Dashboard,
    Filters,
    Format,
    Layout,
    Markers,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuSizeEnum,
    ModeEnum,
    WidgetScatterPlot,
    WidgetTerms,
)

PR_SCHEMA_PATH = (
    'nomad_polymerization_reactions.schema_packages.polymerization.'
    'PolymerizationReaction'
)
polymerization_app = App(
    label='Polymerization Reactions',
    path='polymerization',
    category='Use Cases',
    description='Search app for polymerization reactions entries.',
    readme="""
    Explore all the polymerization reactions with entry type
    **`PolymerizationReaction`**. The filter menu on the left contains several pre-set
    fields that are specifically designed for polymerization reaction exploration.
    The dashboard directly shows useful interactive statistics about the data.
    """,
    filters=Filters(
        include=[
            f'*#{PR_SCHEMA_PATH}',
        ],
    ),
    filters_locked={
        'entry_type': 'PolymerizationReaction',
    },
    columns=[
        Column(
            search_quantity=(
                f'data.reaction_conditions.polymerization_method#{PR_SCHEMA_PATH}'
            ),
            label='Polymerization Method',
            selected=True,
        ),
        Column(
            search_quantity=(
                f'data.reaction_conditions.polymerization_type#{PR_SCHEMA_PATH}'
            ),
            label='Type',
            selected=True,
        ),
        Column(
            search_quantity=f'data.reaction_conditions.solvent.name#{PR_SCHEMA_PATH}',
            label='Solvent',
            selected=True,
        ),
        Column(
            search_quantity=(f'data.reaction_conditions.temperature#{PR_SCHEMA_PATH}'),
            label='Temperature',
            selected=True,
            format=Format(
                decimals=2,
                mode=ModeEnum.STANDARD,
            ),
        ),
        Column(
            search_quantity=(f'data.publication_reference.DOI_number#{PR_SCHEMA_PATH}'),
            label='Publication DOI',
            selected=True,
        ),
    ],
    menu=Menu(
        size=MenuSizeEnum.SM,
        items=[
            Menu(
                title='Reaction Conditions',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemHistogram(
                        title='Temperature',
                        x=Axis(
                            search_quantity=(
                                f'data.reaction_conditions.temperature#{PR_SCHEMA_PATH}'
                            ),
                            scale='linear',
                            unit='K',
                        ),
                    ),
                    MenuItemHistogram(
                        title='Solvent LogP',
                        x=Axis(
                            search_quantity=(
                                'data.reaction_conditions.solvent_descriptors.log_P#'
                                f'{PR_SCHEMA_PATH}'
                            ),
                            scale='linear',
                        ),
                    ),
                    MenuItemTerms(
                        title='Solvent',
                        search_quantity=(
                            f'data.reaction_conditions.solvent.name#{PR_SCHEMA_PATH}'
                        ),
                        width=4,
                        options=10,
                        show_input=True,
                    ),
                    MenuItemTerms(
                        title='Method',
                        search_quantity=(
                            'data.reaction_conditions.polymerization_method#'
                            f'{PR_SCHEMA_PATH}'
                        ),
                        width=4,
                        options=10,
                        show_input=True,
                    ),
                    MenuItemTerms(
                        title='Type',
                        search_quantity=(
                            'data.reaction_conditions.polymerization_type#'
                            f'{PR_SCHEMA_PATH}'
                        ),
                        width=4,
                        options=10,
                        show_input=True,
                    ),
                ],
            ),
            Menu(
                title='Reaction Constants',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemHistogram(
                        title='Reaction Constant',
                        x=Axis(
                            search_quantity=(
                                'data.reaction_conditions.reaction_constants.'
                                f'reaction_constant#{PR_SCHEMA_PATH}'
                            ),
                            scale='linear',
                        ),
                    ),
                    MenuItemTerms(
                        title='Calculation Method',
                        search_quantity=(
                            'data.reaction_conditions.calculation_method#'
                            f'{PR_SCHEMA_PATH}'
                        ),
                        options=10,
                        show_input=True,
                    ),
                ],
            ),
            Menu(
                title='Publication',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemHistogram(
                        title='Publication Date',
                        x=Axis(
                            search_quantity=(
                                'data.publication_reference.publication_date'
                                f'#{PR_SCHEMA_PATH}'
                            ),
                            scale='linear',
                        ),
                    ),
                    MenuItemTerms(
                        title='DOI Number',
                        search_quantity=(
                            f'data.publication_reference.DOI_number#{PR_SCHEMA_PATH}'
                        ),
                        width=6,
                        options=10,
                        show_input=True,
                    ),
                    MenuItemTerms(
                        title='Journal',
                        search_quantity=(
                            f'data.publication_reference.journal#{PR_SCHEMA_PATH}'
                        ),
                        width=6,
                        options=10,
                        show_input=True,
                    ),
                ],
            ),
        ],
    ),
    dashboard=Dashboard(
        # SM: 6x12 grid
        # MD: 9x18 grid
        # LG: 12x24 grid
        # XL: 15x30 grid
        # XXL: 18x36 grid
        widgets=[
            WidgetScatterPlot(
                title='r1 vs r2 colored by Calculation Method',
                autorange=True,
                sample_size=10000,
                y=AxisQuantity(
                    search_quantity=(
                        'data.reaction_conditions.reaction_constants[0].'
                        f'reaction_constant#{PR_SCHEMA_PATH}'
                    ),
                    title='r1',
                ),
                x=AxisQuantity(
                    search_quantity=(
                        'data.reaction_conditions.reaction_constants[1].'
                        f'reaction_constant#{PR_SCHEMA_PATH}'
                    ),
                    title='r2',
                ),
                markers=Markers(
                    color=AxisQuantity(
                        search_quantity=(
                            'data.reaction_conditions.calculation_method'
                            f'#{PR_SCHEMA_PATH}'
                        ),
                        title='Calculation Method',
                    ),
                ),
                layout={
                    BreakpointEnum.XXL: Layout(h=9, w=16, y=0, x=0),
                    BreakpointEnum.XL: Layout(h=8, w=13, y=0, x=0),
                    BreakpointEnum.LG: Layout(h=12, w=16, y=0, x=0),
                    BreakpointEnum.MD: Layout(h=8, w=18, y=0, x=0),
                    BreakpointEnum.SM: Layout(h=6, w=12, y=0, x=0),
                },
            ),
            WidgetScatterPlot(
                title='r-product vs Reaction Temperature',
                autorange=True,
                sample_size=10000,
                y=AxisQuantity(
                    search_quantity=(f'data.r_product#{PR_SCHEMA_PATH}'),
                    title='r-product',
                ),
                x=AxisQuantity(
                    search_quantity=(
                        f'data.reaction_conditions.temperature#{PR_SCHEMA_PATH}'
                    ),
                    title='Reaction Temperature',
                ),
                layout={
                    BreakpointEnum.XXL: Layout(h=9, w=12, y=0, x=16),
                    BreakpointEnum.XL: Layout(h=8, w=10, y=0, x=13),
                    BreakpointEnum.LG: Layout(h=6, w=8, y=0, x=16),
                    BreakpointEnum.MD: Layout(h=8, w=10, y=8, x=0),
                    BreakpointEnum.SM: Layout(h=6, w=12, y=6, x=0),
                },
            ),
            WidgetTerms(
                title='Monomer',
                search_quantity=(f'data.monomers.name#{PR_SCHEMA_PATH}'),
                layout={
                    BreakpointEnum.XXL: Layout(h=9, w=8, y=0, x=28),
                    BreakpointEnum.XL: Layout(h=8, w=7, y=0, x=23),
                    BreakpointEnum.LG: Layout(h=6, w=8, y=6, x=16),
                    BreakpointEnum.MD: Layout(h=8, w=8, y=8, x=10),
                    BreakpointEnum.SM: Layout(h=6, w=12, y=12, x=0),
                },
            ),
        ]
    ),
)
