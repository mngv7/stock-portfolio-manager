SSM = require("@aws-sdk/client-ssm");
const client = new SSM.SSMClient({ region: "ap-southeast-2" });

const paramatersCache = {};

async function fetchParameterAws(parameter_name) {
    try {
        response = await client.send(
        new SSM.GetParameterCommand({
            Name: parameter_name
        }));
    return response.Parameter.Value;
    } catch (error) {
        return null;
    }
}

async function fetchParameterLocal(parameter_name) {
    if (parameter_name in paramatersCache) {
        return paramatersCache[parameter_name];
    } else {
        const parameterValue = await fetchParameterAws(parameter_name);
        if (parameterValue !== null) {
            paramatersCache[parameter_name] = parameterValue;
        }
        return parameterValue;
    }
}

export default fetchParameterLocal;