from django.core.management.base import BaseCommand
from apps.survey.models import Survey, Question
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample survey data'

    def handle(self, *args, **options):
        # Get first user or create one
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username='admin', password='admin123', user_position='ST')

        # Create sample survey
        survey, created = Survey.objects.get_or_create(
            name='Survey Sosial Ekonomi Desa Sumberoto 2025',
            defaults={
                'description': 'Survey untuk mengumpulkan data sosial ekonomi warga desa',
                'year': 2025,
                'is_active': True,
                'created_by': user
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created survey: {survey.name}'))

            # Create sample questions
            questions_data = [
                {
                    'text': 'Berapa pendapatan bulanan Anda?',
                    'question_type': 'choice',
                    'choices': 'Dibawah Rp1jt,Rp1jt - Rp3jt,Rp3jt - Rp5jt,Rp5jt - Rp10jt,Diatas Rp10jt'
                },
                {
                    'text': 'Apakah Anda memiliki pekerjaan tetap?',
                    'question_type': 'choice',
                    'choices': 'Ya,Tidak'
                },
                {
                    'text': 'Berapa jumlah anggota keluarga Anda?',
                    'question_type': 'number'
                },
                {
                    'text': 'Apa pendidikan terakhir Anda?',
                    'question_type': 'choice',
                    'choices': 'SD,SMP,SMA/SMK,D1-D3,S1,S2,S3'
                }
            ]

            for i, q_data in enumerate(questions_data):
                question, q_created = Question.objects.get_or_create(
                    survey=survey,
                    text=q_data['text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'choices': q_data.get('choices', ''),
                        'order': i
                    }
                )
                if q_created:
                    self.stdout.write(f'  Created question: {question.text}')

        else:
            self.stdout.write(f'Survey already exists: {survey.name}')

        self.stdout.write(self.style.SUCCESS('Sample survey data creation completed.'))
