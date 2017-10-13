from tastypie.resources import ModelResource
from tastypie import fields, utils
from ..models import *
from ..AES import AES
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.authentication import *
from django.contrib.auth.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']

class UsuarioResource(ModelResource):
    def obj_get_list(self, bundle, **kwargs):
        return Usuario.objects.all()

    usuario = fields.ToOneField(UserResource, 'usuario', null=True)
    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        #authorization = Authorization()
        #authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }
class MensagemResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        userLogado = bundle.request.user
        usuario = Usuario.objects.get(user = userLogado)
        if usuario:
            msg = Mensagem()
            aes = AES(usuario.chave)
            texto_encriptado = aes.encrypt(bundle.data['mensagem'])
            msg.mensagem = texto_encriptado
            msg.usuario = usuario

            msg.save()
            bundle.obj = msg
            return bundle
        else:
            raise Unauthorized("É necessario ter uma conta cadastrada no sistema!")

    def obj_get(self, bundle, **kwargs):
        userLogado = bundle.request.user
        mensagem = Mensagem.objects.get(pk=int(kwargs['pk']))
        if mensagem.usuario.user == userLogado:
            aes = AES(mensagem.usuario.chave)
            mensagem.mensagem = aes.decrypt(mensagem.mensagem)
            return mensagem
        else:
            raise Unauthorized("Você não tem autorização para visualizar essa mensagem!")

    usuario = fields.ToOneField(UsuarioResource, 'usuario', null=True)
    class Meta:
        queryset = Mensagem.objects.all()
        allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao" : ('exact', 'starswith')
        }