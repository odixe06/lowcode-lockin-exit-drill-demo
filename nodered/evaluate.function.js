const amount = msg.payload && msg.payload.amount;
const policy = global.get('policy');
if (typeof amount !== 'number' || !Number.isSafeInteger(amount) || amount < 0) {
    msg.statusCode = 400;
    msg.payload = {error: 'amount must be a non-negative safe integer'};
} else {
    msg.statusCode = 200;
    msg.payload = {decision: amount <= policy.auto_approve_limit ? 'approved' : policy.otherwise, policy_version: policy.version, currency: policy.currency};
}
return msg;
