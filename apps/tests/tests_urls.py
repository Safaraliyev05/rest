from rest_framework.reverse import reverse_lazy


class TestUrl:
    def test_auth(self):
        url = reverse_lazy('send-email')
        assert url == '/api/v1/send-email/'
        url = reverse_lazy('verify-email')
        assert url == '/api/v1/verify-email/'
