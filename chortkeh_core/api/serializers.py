from rest_framework import serializers


class CreateAccountSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(
        max_length=150, allow_blank=True, allow_null=True)


class UpdateAccountSerializer(serializers.Serializer):

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(
        max_length=150, allow_blank=True, allow_null=True)


class WalletSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255)


class GroupSerializer(serializers.Serializer):

    action_type_choices = (('inc', 'Income'), ('exp', 'Expense'),)
    name = serializers.CharField(max_length=255)
    action_type = serializers.ChoiceField(choices=action_type_choices)


class IncomeTransactionSerializer(serializers.Serializer):

    amount = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True)
    wallet_id = serializers.IntegerField(min_value=1)
    group_id = serializers.IntegerField(min_value=1)


class ExpenseTransactionSerializer(IncomeTransactionSerializer):
    pass


class TransferTransactionSerializer(serializers.Serializer):

    amount = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True)
    source_wallet = serializers.IntegerField(min_value=1)
    target_wallet = serializers.IntegerField(min_value=1)
