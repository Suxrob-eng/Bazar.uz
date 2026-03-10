from django.core.management.base import BaseCommand
from bazar.models import Category

class Command(BaseCommand):
    help = 'Kategoriyalarni qo\'shish'

    def handle(self, *args, **kwargs):
        categories = [
            # Nomi, Slug, Ikon
            ('Elektronika', 'elektronika', 'mobile-alt'),
            ('Telefonlar', 'telefonlar', 'phone'),
            ('Kompyuterlar', 'kompyuterlar', 'laptop'),
            ('Planshetlar', 'planshetlar', 'tablet-alt'),
            ('Fotoapparatlar', 'fotoapparatlar', 'camera'),
            ('TV va Audio', 'tv-audio', 'tv'),
            ('O\'yin konsollari', 'oyin-konsollari', 'gamepad'),
            
            ('Kiyim', 'kiyim', 'tshirt'),
            ('Erkaklar kiyimi', 'erkaklar-kiyimi', 'user-tie'),
            ('Ayollar kiyimi', 'ayollar-kiyimi', 'user'),
            ('Bolalar kiyimi', 'bolalar-kiyimi', 'child'),
            ('Poyabzallar', 'poyabzallar', 'shoe-prints'),
            ('Aksessuarlar', 'aksesuarlar', 'gem'),
            
            ('Transport', 'transport', 'car'),
            ('Yengil avtomobillar', 'yengil-avtomobillar', 'car'),
            ('Mototransport', 'mototransport', 'motorcycle'),
            ('Ehtiyot qismlar', 'ehtiyot-qismlar', 'tools'),
            ('Velosipedlar', 'velosipedlar', 'bicycle'),
            
            ('Uy-joy', 'uy-joy', 'home'),
            ('Kvartiralar', 'kvartiralar', 'building'),
            ('Uylar', 'uylar', 'home'),
            ('Xonalar', 'xonalar', 'door-open'),
            ('Ofislar', 'ofislar', 'building'),
            ('Yer maydonlari', 'yer-maydonlari', 'tree'),
            
            ('Hayvonlar', 'hayvonlar', 'dog'),
            ('Itlar', 'itlar', 'dog'),
            ('Mushuklar', 'mushuklar', 'cat'),
            ('Qushlar', 'qushlar', 'dove'),
            ('Baliqlar', 'baliqlar', 'fish'),
            ('Boshqa hayvonlar', 'boshqa-hayvonlar', 'paw'),
            
            ('Xizmatlar', 'xizmatlar', 'tools'),
            ('Ta\'mirlash', 'tamirlash', 'hammer'),
            ('Tozalash', 'tozalash', 'broom'),
            ('Go\'zallik', 'gozallik', 'spa'),
            ('Kuryer xizmati', 'kuryer', 'truck'),
            ('Ta\'lim', 'talim', 'graduation-cap'),
            
            ('Uy-ro\'zg\'or', 'uy-rozgor', 'couch'),
            ('Mebellar', 'mebellar', 'chair'),
            ('Idish-tovoq', 'idish-tovoq', 'utensils'),
            ('Uy texnikasi', 'uy-texnikasi', 'blender'),
            
            ('Sport', 'sport', 'futbol'),
            ('Sport anjomlari', 'sport-anjomlari', 'basketball-ball'),
            ('Fitnes', 'fitnes', 'dumbbell'),
            ('Turizm', 'turizm', 'hiking'),
            
            ('Kitoblar', 'kitoblar', 'book'),
            ('Darsliklar', 'darsliklar', 'book-open'),
            ('Badiiy kitoblar', 'badiiy-kitoblar', 'book'),
            ('Jurnallar', 'jurnallar', 'newspaper'),
            
            ('Bolalar dunyosi', 'bolalar-dunyosi', 'baby'),
            ('O\'yinchoqlar', 'oyinchoqlar', 'puzzle-piece'),
            ('Bolalar transporti', 'bolalar-transporti', 'baby-carriage'),
            ('Beshliklar', 'beshliklar', 'bed'),
            
            ('Salomatlik', 'salomatlik', 'heartbeat'),
            ('Tibbiy buyumlar', 'tibbiy-buyumlar', 'syringe'),
            ('Parvarish', 'parvarish', 'hand-holding-heart'),
            
            ('Bog\'', 'bog', 'seedling'),
            ('Gullar', 'gullar', 'flower'),
            ('Ko\'chatlar', 'kochatlar', 'tree'),
            ('Bog\' jihozlari', 'bog-jihozlari', 'tractor'),
            
            ('Kolleksiya', 'kolleksiya', 'coins'),
            ('Tangalar', 'tangalar', 'coins'),
            ('Markalar', 'markalar', 'envelope'),
            ('Antiqvarlar', 'antiqvarlar', 'clock'),
            
            ('Ish o\'rinlari', 'ish-orinlari', 'briefcase'),
            ('Vakansiyalar', 'vakansiyalar', 'user-tie'),
            ('Rezyumelar', 'rezyumelar', 'file-alt'),
            
            ('Boshqa', 'boshqa', 'th-large'),
        ]
        
        for name, slug, icon in categories:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Qo'shildi: {name}"))
            else:
                self.stdout.write(f"Mavjud: {name}")
                
        self.stdout.write(self.style.SUCCESS(f"Jami {len(categories)} ta kategoriya qo'shildi/tekshirildi"))

class Command(BaseCommand):
    help = 'Kategoriyalarni qo\'shish'

    def handle(self, *args, **kwargs):
        categories = [
            ('Elektronika', 'elektronika', 'mobile-alt'),
            ('Telefonlar', 'telefonlar', 'phone'),
            ('Kompyuterlar', 'kompyuterlar', 'laptop'),
            # ... qolgan barcha kategoriyalar (sizning ro‘yxatingiz)
            ('Boshqa', 'boshqa', 'th-large'),
        ]
        
        for name, slug, icon in categories:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Qo'shildi: {name}"))
            else:
                self.stdout.write(f"Mavjud: {name}")
                
        self.stdout.write(self.style.SUCCESS(f"Jami {len(categories)} ta kategoriya qo'shildi/tekshirildi"))