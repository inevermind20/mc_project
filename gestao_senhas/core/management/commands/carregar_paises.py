from django.core.management.base import BaseCommand
from core.models import Pais

class Command(BaseCommand):
    help = 'Carrega lista de países'

    def handle(self, *args, **kwargs):
        paises = [
            ('PT', 'PORTUGAL'),
            ('ES', 'ESPANHA'),
            ('FR', 'FRANÇA'),
            ('DE', 'ALEMANHA'),
            ('IT', 'ITÁLIA'),
            ('GB', 'REINO UNIDO'),
            ('NL', 'HOLANDA'),
            ('BE', 'BÉLGICA'),
            ('CH', 'SUÍÇA'),
            ('AT', 'ÁUSTRIA'),
            ('SE', 'SUÉCIA'),
            ('NO', 'NORUEGA'),
            ('DK', 'DINAMARCA'),
            ('FI', 'FINLÂNDIA'),
            ('PL', 'POLÓNIA'),
            ('CZ', 'REPÚBLICA CHECA'),
            ('HU', 'HUNGRIA'),
            ('RO', 'ROMÉNIA'),
            ('GR', 'GRÉCIA'),
            ('IE', 'IRLANDA'),
            ('LU', 'LUXEMBURGO'),
            ('BR', 'BRASIL'),
            ('US', 'ESTADOS UNIDOS'),
            ('CN', 'CHINA'),
            ('JP', 'JAPÃO'),
            ('IN', 'ÍNDIA'),
        ]

        for codigo, designacao in paises:
            Pais.objects.get_or_create(codigo=codigo, defaults={'designacao': designacao})

        self.stdout.write(self.style.SUCCESS(f'✓ {len(paises)} países carregados!'))
