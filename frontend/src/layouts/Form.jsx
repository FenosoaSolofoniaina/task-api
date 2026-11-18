import { CustomBlueInput, CustomBlueCheckBox, CustomBlueRadio, CustomBlueSelect } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";



function renderFields(field, index) {

    switch(field.format) {
        case "input" :
            return (
                <CustomBlueInput
                    key={index}
                    {...field.attributes} 
                    label={field.text} />
            );

        case "checkbox":
            return (
                <CustomBlueCheckBox
                    key={index}
                    {...field.attributes} 
                    label={field.text} />
                
            );

        case "radio":
            let groupName = field.group.name;
            
            return (
                <fieldset id={groupName} key={index} >
                    <legend className="font-bold" >
                        {field.text}
                    </legend>
                    <div className="flex flex-row justify-around" >
                        {
                            field.group.items.map( group => <CustomBlueRadio
                                key={group.attributes.value}
                                name={groupName}
                                label={group.text}
                                {...group.attributes} />
                            )
                        }
                    </div>
                        
                </fieldset>
            );

        case "select":
            return (
                <CustomBlueSelect
                    key={index}
                    textLabel={field.text}
                    {...field.attributes} >
                    {
                        field.options.map( option => <option key={option.key}
                                                            value={option.value}
                                                            name={option.name} >
                                                        {option.text}
                                                    </option>)
                    }
                </CustomBlueSelect>
            );

        case "submit" :
            return (
                <CustomBlueSubmitButton key={index}
                    {...field.attributes} >
                    {field.text}
                </CustomBlueSubmitButton>
            );
    }

}


export function FormLayout({ fields, onSubmit }) {

    return (
        <form onSubmit={onSubmit} autoComplete="false" aria-required >
            { fields.map( (field, i) => renderFields(field, i)) }
        </form>
    );
}