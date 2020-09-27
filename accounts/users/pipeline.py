def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    icon_url = None
    bg_url = None
    descripton = None
    if backend.name == 'twitter':
        icon_url = response.get('profile_image_url', '').replace('_normal','')
        bg_url = response.get('profile_banner_url', '')
        description = response.get('description', '')
    if icon_url and bg_url and description:
        user.icon_url = icon_url
        user.bg_url = bg_url
        user.description = description
        user.save()
