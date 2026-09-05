# Django / Python Rules

```
❌ Don't                             ✅ Do
------------------------------------------------------
Business logic in views.py           Put in service layer / model method
Duplicate querysets in views         Extract to Manager method
Raw SQL without strong reason        Use the ORM
> 25 lines per method                Extract method
Nested serializers without reason    Flatten or use SerializerMethodField
```

**Correct layer structure:**
```
views.py       → request/response + input validation only
serializers.py → data transformation only
services.py    → business logic lives here
models.py      → data + simple model methods
managers.py    → custom queryset logic
```

**Duplicated querysets → Manager:**
```python
# models.py
class UserManager(models.Manager):
    def active(self):
        return self.filter(is_active=True).select_related('profile')

# views.py
users = User.objects.active()
```

**Thin view:**
```python
# ✅ Good
class UserListView(APIView):
    def get(self, request):
        users = UserService.get_active_users(request.user)
        return Response(UserSerializer(users, many=True).data)

# ❌ Bad
class UserListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True, role='member')
        if request.user.is_admin:
            users = users.filter(department=request.user.department)
        # ... 30 more lines
```
