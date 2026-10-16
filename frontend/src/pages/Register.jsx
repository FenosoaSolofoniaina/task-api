import { CustomBlueLink } from "../components/Ancres";
import { CustomBlueInput, CustomBlueSelect } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";
import { CustomH2MediumTitle } from "../components/Titles";



function PersonalRegisterForm({ personalForms, listCountries }) {

    return (
        <div className="my-[3em]" >
            <CustomH2MediumTitle>
                Informations personnelles
                <hr />
            </CustomH2MediumTitle>
            {
                personalForms.map(loginItem => <CustomBlueInput
                            key={loginItem.id}
                            id={loginItem.id}
                            type={loginItem.type}
                            placeholder={loginItem.placeholder}
                            title={loginItem.title} >
                        {loginItem.text}
                    </CustomBlueInput>
                )
            }
            <CustomBlueSelect textLabel="Sélectionner votre pays d'origine" >
                {
                    listCountries.map(country => <option
                                key={country.id}
                                value={country.id} >
                            {country.text}
                        </option>
                    )
                }
            </CustomBlueSelect>
        </div>
    );
}


function AccountRegisterForm({ accountForms }) {

    return (
        <div className="my-[3em]" >
            <CustomH2MediumTitle>
                Informations de compte
                <hr />
            </CustomH2MediumTitle>
            {
                accountForms.map(loginItem => <CustomBlueInput
                            key={loginItem.id}
                            id={loginItem.id}
                            type={loginItem.type}
                            placeholder={loginItem.placeholder}
                            title={loginItem.title} >
                        {loginItem.text}
                    </CustomBlueInput>
                )
            }
        </div>
    );
}


function BackToLoginForm() {

    const textLink = "Se connecter";

    return (
        <div className="flex flex-row justify-center items-center m-y-[1em]" >
            <p>
                Vous avez dèjà un compte ?  
            </p>
            <CustomBlueLink hrefLink="/login" 
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function RegisterPage() {

    function sendRegisterForm(event) {
        event.preventDefault();
        event.stopPropagation();

        alert('Register done');
    }

    const personalFormStructures = [
        {
            "id": "first-name",
            "type": "text",
            "placeholder": "Ex: Doe",
            "title": "Nom",
            "text": "Nom"
        },
        {
            "id": "last-name",
            "type": "text",
            "placeholder": "Ex: John",
            "title": "Prénom",
            "text": "Prénom"
        },
        {
            "id": "birth",
            "type": "date",
            "placeholder": "",
            "title": "Date de naissance",
            "text": "Date de naissance"
        }
    ];

    const accountFormStructures = [
        {
            "id": "identity",
            "type": "text",
            "placeholder": "",
            "title": "Identifiant",
            "text": "Identifiant"
        },
        {
            "id": "password",
            "type": "password",
            "placeholder": "",
            "title": "Mot de passe",
            "text": "Mot de passe"
        },
        {
            "id": "confirme-password",
            "type": "password",
            "placeholder": "",
            "title": "Confirmer le mot de passe",
            "text": "Confirmer le mot de passe"
        },
    ];

    const countries = [
        {
            "id": "",
            "text": "Selectionner ..."
        },
        {
            "id": "MDG",
            "text": "Madagascar"
        },
        {
            "id": "FR",
            "text": "France"
        },
        {
            "id": "ES",
            "text": "Espagne"
        },
        {
            "id": "DE",
            "text": "Allemagne"
        },
        {
            "id": "USA",
            "text": "Etats-Unis"
        }
    ]

    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                <CustomH2MediumTitle>
                    Créér un nouveau compte
                </CustomH2MediumTitle>
                <form method="post" onSubmit={sendRegisterForm}>
                    <PersonalRegisterForm personalForms={personalFormStructures} 
                                          listCountries={countries} />
                    <AccountRegisterForm accountForms={accountFormStructures} />
                    <CustomBlueSubmitButton>
                        Créér mon compte
                    </CustomBlueSubmitButton>
                </form>
                <BackToLoginForm />
            </div>
        </div>
    )
}


export default RegisterPage; 