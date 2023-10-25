

'''
def create_shortcode(instance, size=SHORT_CODE_LENGTH):
    new_code = code_generator(size)
    Arena = instance.__class__  # way to avoid circling around import
    query_exists = Arena.objects.filter(short_code=new_code).exists()
    if query_exists:
        return create_shortcode(instance=instance, size=size)
    return new_code


def code_generator(size=SHORT_CODE_LENGTH, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
'''

example = 'PL / Mazowieckie / Warszawa'
name = example.split('/')
def create_arena(identyfier, parent):
    