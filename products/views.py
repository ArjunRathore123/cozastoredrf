from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProductSerializer,CartSerializer,OrderSerialzier
from .models import Category,Product,Size,Cart,Order
from accounts.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.conf import settings
# Create your views here.

class ProductView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            product=Product.objects.all()
            if product:
                serailizer=ProductSerializer(product,many=True)
                return Response({
                    'success':True,
                    'status':status.HTTP_200_OK,
                    'data':serailizer.data
                })
            return Response({
                    'success':False,
                    'status':status.HTTP_404_NOT_FOUND,
                    'data':{}
                })
        except Product.DoesNotExist:
            return Response({
                'success':False,
                status:status.HTTP_400_BAD_REQUEST,
                'data':serailizer.errors
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })
        

    def post(self, request, *args, **kwargs):
        category_id=request.query_params.get('category_id')
        try:
            category=Category.objects.get(id=category_id)
            if request.user.user_type=='seller':
                data=request.data
                name=data['product_name']
                image=data['product_image']
                amt=data['price']
                qty=data['quantity']
                desc=data['description']
                size=data.get('size',[])
                    
                sizes_list = [size.strip() for size in size.split(',')]
                size = [Size.objects.get_or_create(size=size)[0] for size in sizes_list]

                product=Product.objects.create(product_name=name,product_image=image,price=amt,quantity=qty,description=desc,category=category)
                product.size.set(size)

                return Response({
                    'success':True,
                    'status':status.HTTP_201_CREATED,
                    'data':ProductSerializer(product).data
                })
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Category not found'}
            })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })
        
    def put(self,request,*args, **kwargs):
        category_id=request.query_params.get('category_id')
        product_id=request.query_params.get('product_id')
        try:
            category=Category.objects.get(id=category_id)
            product=Product.objects.get(id=product_id)
            if request.user.user_type=='seller':
                data=request.data
                name=data['product_name']
                image=data['product_image']
                amt=data['price']
                qty=data['quantity']
                desc=data['description']
                size=data.get('size',[])
                size=[size.strip() for size in size.split(',')]
                
                product.product_image=image
                product.product_name=name
                product.price=amt
                product.quantity=qty
                product.description=desc
                product.category=category

                size = [Size.objects.get_or_create(size=size)[0] for size in size]
                product.size.set(size)
                product.save()

                return Response({
                    'success':True,
                    'status':status.HTTP_200_OK,
                    'data':ProductSerializer(product).data
                })
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Category not found'}
            })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })
        
    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            if request.user.user_type=='seller':
                product=Product.objects.get(id=product_id)
                
                product.delete()
                return Response({
                    'success':True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'data':{'msg':'Delete Successfully'}
                })
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })

class CartView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            if request.user.user_type=='buyer':
                product=Product.objects.get(id=product_id)
                cart,created=Cart.objects.get_or_create(product=product,user=request.user)
                if product.quantity > 0:
                    product.quantity-=1
                    product.save()
                    if not created:
                        cart.quantity+=1              
                        cart.save()
                    return Response({
                        'success': True,
                        'status':status.HTTP_201_CREATED,
                        'data':CartSerializer(cart).data
                    }) 
                return Response({
                        'success': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'data': 'Product out of stock'
                    })
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Cart.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Cart not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })

    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            if request.user.user_type=='buyer':
                product=Product.objects.get(id=product_id)
                cart=Cart.objects.get(product=product,user=request.user)
                if cart.qunatity>=1 and cart.qunatity is not None:
                    product.quantity+=cart.qunatity
                    product.save()
                cart.delete()
                return Response({
                    'success': True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'data':{'msg':'Cart Deleted'}
                }) 
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })
            
    
class QuantityView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        product=request.query_params.get('product_id')
        action=request.query_params.get('action')
        try:
            if request.user.user_type=='buyer':
                product=Product.objects.get(id=product)
                cart=Cart.objects.get(product=product,user=request.user)
                if action=='increase':
                    if product.quantity > 0:
                        cart.qunatity+=1
                        product.quantity-=1
                        cart.save()
                        product.save()
                        return Response({
                        'success': True,
                        'status':status.HTTP_200_OK,
                        'data':CartSerializer(cart).data
                        }) 
                    return Response({
                        'success': True,
                        'status':status.HTTP_400_BAD_REQUEST,
                        'data':'Out of Stock'
                    }) 
                elif action == 'decrease':
                    if cart.qunatity > 1:
                        product.quantity+=1
                        cart.qunatity-=1
                        product.save()
                        cart.save()
                        return Response({
                            'success': True,
                            'status':status.HTTP_200_OK,
                            'data':CartSerializer(cart).data
                        }) 
                    else:
                        product.quantity+=1
                        product.save()
                        cart.delete()
                        return Response({
                            'success': True,
                            'status':status.HTTP_200_OK,
                            'data':'Cart Item Deleted'
                        }) 
            return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Cart.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': {'error': 'Product not found'}
            })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': {'error': str(e)}
            })

class CreateOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        if request.user.user_type=='buyer':
            product_id=request.query_params.get('product_id')
            product=Product.objects.get(id=product_id)
            user=CustomUser.objects.get(id=request.user.id)
            cart=Cart.objects.filter(user=user)

            if not cart.exists():
                return Response({
                    'success': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Cart is empty'
                })
            data=request.data
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            address=data.get('address')
            pincode=data.get('pincode')
            contact=data.get('contact')
            city=data.get('city')
            email=data.get('email') 
            order={
                'user':user.id,
                'product':product.id,
                'city':city,
                'pincode':pincode,
                'first_name':first_name,
                'last_name':last_name,
                'address':address,
                'email':email,
                'contact':contact
            }
            serializer=OrderSerialzier(data=order)
            if serializer.is_valid():
                order=serializer.save()
                for item in cart:
                    price=item.quantity * item.product.price
                client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
                payment=client.order.create({'amount': price*100, "currency": "INR", 'payment_capture': 1})
                order.razorpay_order_id=payment['id']

                cart.delete()
                order.save()
                return Response(
                    {'success':True,
                    'status':status.HTTP_201_CREATED,
                    'msg':'Order Created',
                    'data':serializer.data}
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                    'success':False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'data':'Unauthorized User'
                })

# class PaymentSuccessView(APIView):
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[JWTAuthentication]
#     def put(self, request, *args, **kwargs):
#         order_id=request.query_params.get('order_id')
#         if request.user.user_type=='buyer':
#             user=CustomUser.objects.get(id=request.user.id)
#             order=

#         return Response({
#                     'success':False,
#                     'status':status.HTTP_401_UNAUTHORIZED,
#                     'data':'Unauthorized User'
#                 })


        