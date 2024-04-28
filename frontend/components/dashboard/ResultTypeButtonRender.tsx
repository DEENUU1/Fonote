import {resultType} from "@/components/dashboard/const";
import {Button} from "@nextui-org/react";


export default function ResultTypeButtonRender(
	{
		handleResponseCreate,
		detailInputData,
		isLoading
	}:
	{
		handleResponseCreate: (id: any, resultType: any) => void,
		detailInputData: any,
		isLoading: boolean
	}
){

	return (
		<>
		{resultType.map((resultType, index) => (
			<div key={index} className={"mt-5 gap-2"}>
				<Button className={"mr-2"} variant={"ghost"} size={"sm"} isLoading={isLoading} type={"button"}
								onClick={() => handleResponseCreate(detailInputData?.id, resultType)}>
					{resultType}
				</Button>
			</div>
		))}
		</>
	)
}