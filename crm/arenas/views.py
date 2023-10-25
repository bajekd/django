

"""
        if not Arena.objects.filter(identifier=form.cleaned_data['identifier']).exists():
            if not Arena.objects.filter(identifier=f"{country}/{region}").exists():
                if not Arena.objects.filter(identifier=f"{country}").exists():
                    if not Arena.objects.filter(identifier="/").exists():
                        Arena.objects.create(identifier='/')

                    Arena.objects.create(identifier=f"{country}")
                Arena.objects.create(identifier=f"{country}/{region}")
            Arena.objects.create(identifier=f"{form.cleaned_data['identifier']}")
        return super().form_vaild(form)
"""
#parent = Arena.objects.get_or_create(identifier__endswith=region, parent=Arena.objects.get(identifier=country))
              #Arena.objects.get_or_create(identifier=identifier, parent=parent.id)