from forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    u = get_object_or_404(User, username=username)
    p = u.post_set.all().order_by('-date_posted')

    # code to get followers of a user
    followers = []
    all_users = User.objects.all()
    print(all_users)  # sanity check
    for user in all_users:
        if u.profile in user.profile.follows.all():
            print(user.username + ' follows ' + u.username)  # sanity check
            followers.append(user)
            print(followers)  # sanity check
            print(len(followers))  # sanity check
    no_of_followers = len(followers)

    context = {
        'u': u,
        'p': p,
        'followers': followers,
        'n_o_f': no_of_followers
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account updated!')
            return redirect('profile', request.user.username)


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)


@login_required
def follow_toggle(request):
    if request.method == 'GET':
        u_t_f = request.GET.get("userToFollow")
        u_f = request.GET.get("userFollowing")

        user_to_follow = User.objects.get(username=u_t_f)
        user_following = User.objects.get(username=u_f)

        if user_to_follow.profile in user_following.profile.follows.all():
            user_following.profile.follows.remove(user_to_follow.profile)
        else:
            user_following.profile.follows.add(user_to_follow.profile)

        data={
            'hello': 'hello'
        }

        return JsonResponse(data)


def following(request, username):
    user = User.objects.get(username=username)
    following_users_profile = user.profile.follows.all()

    context = {
        'f_u_p': following_users_profile
    }
    return render(request, 'users/following.html', context)
