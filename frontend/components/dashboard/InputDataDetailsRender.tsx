import {Chip} from "@nextui-org/react";


export default function InputDataDetailsRender({detailInputData}: {detailInputData: any}){
	return (
	<>
		{detailInputData?.fragments.length > 0 && (
			<div className="w-full flex mb-4 gap-2">
				<Chip color={"default"}
							variant={"bordered"}>{detailInputData?.audio_length_minutes} minutes</Chip>
				<Chip color={"default"} variant={"bordered"}>{detailInputData?.language}</Chip>
				<Chip color={"default"} variant={"bordered"}>{detailInputData?.source}</Chip>
				<Chip color={"default"} variant={"bordered"}>{detailInputData?.transcription_type}</Chip>
			</div>
		)
		}
	</>
	)
}