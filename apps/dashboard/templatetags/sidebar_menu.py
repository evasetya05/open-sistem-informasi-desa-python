from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def get_sidebar_menu(context):
    request = context.get('request')
    user = getattr(request, 'user', None)
    
    menu_items = []
    
    # Dashboard
    menu_items.append({
        'title': 'Dashboard',
        'icon': 'fa-tachometer-alt',
        'url': reverse('dashboard:index'),
        'is_active': request.resolver_match.app_name == 'dashboard',
        'children': []
    })
    
    # Kependudukan
    kependudukan_children = []
    if user.has_perm('kependudukan.view_penduduk'):
        kependudukan_children.append({
            'title': 'Data Penduduk',
            'url': reverse('kependudukan:penduduk_list'),
            'is_active': 'penduduk' in request.resolver_match.url_name
        })
    if user.has_perm('kependudukan.view_kartukeluarga'):
        kependudukan_children.append({
            'title': 'Kartu Keluarga',
            'url': reverse('kependudukan:kk_list'),
            'is_active': 'kk' in request.resolver_match.url_name
        })
    
    if kependudukan_children:
        menu_items.append({
            'title': 'Kependudukan',
            'icon': 'fa-users',
            'url': '#',
            'is_active': request.resolver_match.app_name == 'kependudukan',
            'children': kependudukan_children
        })
    
    # Layanan
    if user.has_perm('layanan.view_antrian'):
        layanan_children = [
            {
                'title': 'Daftar Antrian',
                'url': reverse('daftar_antrian'),
                'is_active': 'daftar_antrian' in request.resolver_match.url_name
            },
            {
                'title': 'Panggil Antrian',
                'url': reverse('panggil_antrian'),
                'is_active': 'panggil_antrian' in request.resolver_match.url_name
            },
            {
                'title': 'Riwayat Antrian',
                'url': reverse('riwayat_antrian'),
                'is_active': 'riwayat_antrian' in request.resolver_match.url_name
            }
        ]
        
        menu_items.append({
            'title': 'Layanan',
            'icon': 'fa-clipboard-list',
            'url': '#',
            'is_active': request.resolver_match.app_name == 'layanan',
            'children': layanan_children
        })
    
    # Survey
    if user.has_perm('survey.view_survey'):
        survey_children = [
            {
                'title': 'Daftar Survey',
                'url': reverse('survey:survey_list'),
                'is_active': 'survey_list' in request.resolver_match.url_name
            },
            {
                'title': 'Survey Saya',
                'url': reverse('survey:my_surveys'),
                'is_active': 'my_surveys' in request.resolver_match.url_name
            }
        ]
        
        menu_items.append({
            'title': 'Survey',
            'icon': 'fa-poll',
            'url': '#',
            'is_active': request.resolver_match.app_name == 'survey',
            'children': survey_children
        })
    
    # Aset
    if user.has_perm('aset.view_aset'):
        menu_items.append({
            'title': 'Manajemen Aset',
            'icon': 'fa-boxes',
            'url': reverse('aset:aset_list'),
            'is_active': request.resolver_match.app_name == 'aset',
            'children': []
        })
    
    # Blog
    if user.has_perm('blog.view_post'):
        blog_children = [
            {
                'title': 'Artikel',
                'url': reverse('blog:post_list'),
                'is_active': 'post_list' in request.resolver_match.url_name
            },
            {
                'title': 'Kategori',
                'url': reverse('blog:category_list'),
                'is_active': 'category' in request.resolver_match.url_name
            }
        ]
        
        menu_items.append({
            'title': 'Blog',
            'icon': 'fa-blog',
            'url': '#',
            'is_active': request.resolver_match.app_name == 'blog',
            'children': blog_children
        })
    
    # Admin Section (for superusers)
    if user.is_superuser:
        admin_children = [
            {
                'title': 'Admin Site',
                'url': reverse('admin:index'),
                'is_active': False
            },
            {
                'title': 'Users',
                'url': reverse('admin:user_user_changelist'),
                'is_active': False
            },
            {
                'title': 'Groups',
                'url': reverse('admin:auth_group_changelist'),
                'is_active': False
            }
        ]
        
        menu_items.append({
            'title': 'Administrasi',
            'icon': 'fa-cog',
            'url': '#',
            'is_active': False,
            'children': admin_children
        })
    
    return {'menu_items': menu_items}

@register.inclusion_tag('dashboard/partials/sidebar_menu.html', takes_context=True)
def render_sidebar_menu(context):
    return get_sidebar_menu(context)
