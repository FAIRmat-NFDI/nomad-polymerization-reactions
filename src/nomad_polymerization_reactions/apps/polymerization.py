import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Filters,
    Format,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuSizeEnum,
    ModeEnum,
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
    dashboard={
        'widgets': yaml.safe_load(f"""
- type: scatter_plot
  autorange: true
  sample_size: 10000
  y:
    search_quantity: data.r_product#{PR_SCHEMA_PATH}
    title: r-product
  x:
    search_quantity: data.reaction_conditions.temperature#{PR_SCHEMA_PATH}
    title: Reaction Temperature
  title: r-product vs Reaction Temperature
  layout:
    xxl:
      minH: 3
      minW: 3
      h: 7
      w: 10
      y: 0
      x: 0
    xl:
      minH: 3
      minW: 3
      h: 9
      w: 12
      y: 0
      x: 11
    lg:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 9
    md:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 0
    sm:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 0
- type: terms
  scale: linear
  search_quantity: data.monomers.name#{PR_SCHEMA_PATH}
  title: Monomer
  layout:
    xxl:
      minH: 3
      minW: 3
      h: 7
      w: 7
      y: 0
      x: 19
    xl:
      minH: 3
      minW: 3
      h: 9
      w: 6
      y: 0
      x: 23
    lg:
      minH: 3
      minW: 3
      h: 9
      w: 6
      y: 0
      x: 18
    md:
      minH: 3
      minW: 3
      h: 9
      w: 6
      y: 0
      x: 0
    sm:
      minH: 3
      minW: 3
      h: 9
      w: 6
      y: 0
      x: 0
- type: scatter_plot
  autorange: true
  sample_size: 10000
  markers:
    color:
      search_quantity: data.reaction_conditions.calculation_method#{PR_SCHEMA_PATH}
      title: Calculation Method
  y:
    search_quantity: data.reaction_conditions.reaction_constants[0].reaction_constant#{PR_SCHEMA_PATH}
    title: r1
  x:
    search_quantity: data.reaction_conditions.reaction_constants[1].reaction_constant#{PR_SCHEMA_PATH}
    title: r2
  title: "r1 vs r2 colored by Calculation Method"
  layout:
    xxl:
      minH: 3
      minW: 3
      h: 7
      w: 9
      y: 0
      x: 10
    xl:
      minH: 3
      minW: 3
      h: 9
      w: 11
      y: 0
      x: 0
    lg:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 0
    md:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 0
    sm:
      minH: 3
      minW: 3
      h: 6
      w: 9
      y: 0
      x: 0

""")  # noqa: E501
    },
)
