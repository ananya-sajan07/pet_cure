from django.shortcuts import render,redirect
from .models import *
from userapp.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views here.

# class DoctorRegistrationView(viewsets.ModelViewSet):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#     http_method_names = ['post']  # only POST allowed

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response({
#                 "status": "success",
#                 "message": "Doctor Registered Successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response({
#                 "status": "failed",
#                 "message": "Invalid Details",
#                 "errors": serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

class DoctorRegistrationView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['post']  # only POST allowed

    def create(self, request, *args, **kwargs):

        # ✅ Check duplicate email
        email = request.data.get("email")
        if email and Doctor.objects.filter(email=email).exists():
            return Response({
                "status": "failed",
                "message": "Email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": "success",
                "message": "Doctor Registered Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

            
            
class DoctorLoginAPIView(APIView):
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                doctor = Doctor.objects.get(email=email, password=password)
            except Doctor.DoesNotExist:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            if doctor.status != 'approved':
                return Response({"error": "Your account is not approved yet"}, status=status.HTTP_403_FORBIDDEN)

            # Successful login
            data = {
                "id": doctor.id,
                "full_name": doctor.full_name,
                "email": doctor.email,
                "phone_number": doctor.phone_number,
                "address": doctor.address,
                "image": f"media/{doctor.image.name}" if doctor.image else None,
                "id_card": f"media/{doctor.id_card.name}" if doctor.id_card else None,
            }

            return Response({"message": "Login successful", "doctor": data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DoctorProfileView(APIView):
    def get(self, request):
        doctor_id = request.query_params.get('doctor_id')

        if not doctor_id:
            return Response({"error": "doctor_id is required as a query parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(id=doctor_id, status='approved')
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found or not approved."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor)
        return Response({"doctor_profile": serializer.data}, status=status.HTTP_200_OK) 
    
    
# class TodayBookingsAPIView(APIView):
#     """
#     GET /doctor/today-bookings/?doctor_id=<id>
#     Returns today's appointments for the specified doctor.
#     """

#     def get(self, request):
#         doctor_id = request.query_params.get('doctor_id')

#         # ✅ 1. Validate doctor_id
#         if not doctor_id:
#             return Response({"error": "doctor_id query parameter is required."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # ✅ 2. Check doctor exists
#         try:
#             doctor = Doctor.objects.get(id=doctor_id)
#         except Doctor.DoesNotExist:
#             return Response({"error": "Doctor not found."},
#                             status=status.HTTP_404_NOT_FOUND)

#         # ✅ 3. Get today's date
#         today = date.today()

#         # ✅ 4. Fetch all appointments for today
#         appointments = Appointment.objects.filter(doctor=doctor, date=today).select_related('pet', 'slot')

#         # ✅ 5. Format response data
#         data = []
#         for appointment in appointments:
#             data.append({
#                 "appointment_id": appointment.id,
#                 "pet": {
#                     "id": appointment.pet.id,
#                     "name": appointment.pet.name,
#                     "category": appointment.pet.category.petcategory,
#                     "sub_category": appointment.pet.sub_category.petsubcategory,
#                     "gender": appointment.pet.gender,
#                     "weight": appointment.pet.weight,
#                 },
#                 "date": str(appointment.date),
#                 "slot": f"{appointment.slot.start_time.strftime('%H:%M')} - {appointment.slot.end_time.strftime('%H:%M')}" if appointment.slot else None,
#                 "reason": appointment.reason,
#                 "symptoms": appointment.symptoms if appointment.reason != "Vaccine" else None,
#                 "booking_option": "Clinical appointment"
#             })

#         return Response({
#             "doctor_name": doctor.full_name,
#             "total_bookings": len(data),
#             "bookings": data
#         }, status=status.HTTP_200_OK)

# class TodayBookingsAPIView(APIView):
#     """
#     GET /doctor/today-bookings/?doctor_id=<id>
#     Returns today's appointments for the specified doctor.
#     """

#     def get(self, request):
#         doctor_id = request.query_params.get('doctor_id')

#         # Validate doctor_id
#         if not doctor_id:
#             return Response({"error": "doctor_id query parameter is required."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # Check doctor exists
#         try:
#             doctor = Doctor.objects.get(id=doctor_id)
#         except Doctor.DoesNotExist:
#             return Response({"error": "Doctor not found."},
#                             status=status.HTTP_404_NOT_FOUND)

#         today = date.today()

#         appointments = Appointment.objects.filter(
#             doctor=doctor, 
#             date=today
#         ).select_related('pet', 'slot')

#         data = []
#         for appointment in appointments:

#             # Slot format
#             slot_time = (
#                 f"{appointment.slot.start_time.strftime('%H:%M')} - "
#                 f"{appointment.slot.end_time.strftime('%H:%M')}"
#                 if appointment.slot else None
#             )

#             # Booking type readable text
#             booking_type = (
#                 "Clinical Appointment"
#                 if appointment.appointment_type == "clinical"
#                 else "Audio Call Appointment"
#             )

#             data.append({
#                 "appointment_id": appointment.id,
#                 "appointment_type": appointment.appointment_type,
#                 # "booking_type": booking_type,

#                 "pet": {
#                     "id": appointment.pet.id,
#                     "name": appointment.pet.name,
#                     "category": appointment.pet.category.petcategory,
#                     "sub_category": appointment.pet.sub_category.petsubcategory,
#                     "gender": appointment.pet.gender,
#                     "weight": appointment.pet.weight,
#                 },

#                 "date": str(appointment.date),

#                 # 🔥 Slot details
#                 "slot_id": appointment.slot.id if appointment.slot else None,
#                 "slot": slot_time,

#                 # Reason only for clinical
#                 "reason": appointment.reason if appointment.appointment_type == "clinical" else None,

#                 # Symptoms allowed for both
#                 "symptoms": appointment.symptoms,

#                 # "notes": appointment.notes,
#             })

#         return Response({
#             "doctor_name": doctor.full_name,
#             "total_bookings": len(data),
#             "bookings": data
#         }, status=status.HTTP_200_OK)

class TodayBookingsAPIView(APIView):
    def get(self, request):
        doctor_id = request.query_params.get('doctor_id')

        if not doctor_id:
            return Response({"error": "doctor_id query parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."},
                            status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        # ⛔ EXCLUDE completed appointments
        appointments = Appointment.objects.filter(
            doctor=doctor,
            date=today,
            diagnosis_and_verdict__isnull=True
        ).select_related('pet', 'slot')

        data = []
        for appointment in appointments:

            slot_time = (
                f"{appointment.slot.start_time.strftime('%H:%M')} - "
                f"{appointment.slot.end_time.strftime('%H:%M')}"
                if appointment.slot else None
            )

            data.append({
                "appointment_id": appointment.id,
                "appointment_type": appointment.appointment_type,

                "pet": {
                    "id": appointment.pet.id,
                    "name": appointment.pet.name,
                    "category": appointment.pet.category.petcategory,
                    "sub_category": appointment.pet.sub_category.petsubcategory,
                    "gender": appointment.pet.gender,
                    "weight": appointment.pet.weight,
                },

                "date": str(appointment.date),

                "slot_id": appointment.slot.id if appointment.slot else None,
                "slot": slot_time,

                "reason": appointment.reason if appointment.appointment_type == "clinical" else None,
                "symptoms": appointment.symptoms,
            })

        return Response({
            "doctor_name": doctor.full_name,
            "total_bookings": len(data),
            "bookings": data
        }, status=status.HTTP_200_OK)

        
class BookingDetailsAPIView(APIView):
    def get(self, request):
        booking_id = request.query_params.get('booking_id')
        if not booking_id:
            return Response(
                {"success": False, "message": "Booking ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = get_object_or_404(Appointment, id=booking_id)
        serializer = AppointmentSerializer(booking)

        return Response({
            "success": True,
            "message": "Booking details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
class CompleteAppointmentAPIView(APIView):
    """
    PATCH - Complete a clinical appointment
    Input:
        - booking_id (Appointment ID)
        - weight
        - diagnosis and verdict
        - notes (optional)
    Output:
        - success message
    """

    def patch(self, request):
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response(
                {"error": "booking_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment = get_object_or_404(Appointment, id=booking_id)
        serializer = AppointmentUpdateSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Update pet's weight if provided
            weight = serializer.validated_data.get('weight')
            if weight is not None:
                pet = appointment.pet
                pet.weight = weight
                pet.save(update_fields=['weight'])

            return Response(
                {"success": True, "message": "Appointment completed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TreatmentHistoryAPIView(APIView):
    def get(self, request):
        doctor_id = request.query_params.get('doctor_id')
        date = request.query_params.get('date')

        if not doctor_id or not date:
            return Response(
                {"error": "Both doctor_id and date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Get only completed treatments
        appointments = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            diagnosis_and_verdict__isnull=False
        ).exclude(
            diagnosis_and_verdict__exact=''
        )

        serializer = TreatmentHistorySerializer(appointments, many=True)

        return Response({
            "success": True,
            "doctor_id": doctor_id,
            "date": date,
            "treatments": serializer.data
        }, status=status.HTTP_200_OK)

        
class TreatmentDetailAPIView(APIView):
    """
    GET - Fetch treatment details for a given appointment (booking)
    Input:
        booking_id (required)
    Output:
        Full treatment, doctor, and pet details (image paths start with media/)
    """

    def get(self, request):
        booking_id = request.query_params.get('booking_id')

        if not booking_id:
            return Response(
                {"error": "booking_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment = get_object_or_404(Appointment, id=booking_id)
        doctor = appointment.doctor
        pet = appointment.pet

        # Get relative image paths (media/...)
        pet_image = pet.pet_image.url if pet.pet_image else None
        doctor_image = doctor.image.url if doctor.image else None
        doctor_id_card = doctor.id_card.url if doctor.id_card else None

        treatment_data = {
            "booking_id": appointment.id,
            "appointment_type": appointment.appointment_type,
            "date": appointment.date,
            "slot": str(appointment.slot),
            "reason": appointment.reason,
            "symptoms": appointment.symptoms,
            "diagnosis": appointment.diagnosis_and_verdict,
            # "verdict": appointment.verdict,
            "notes": appointment.notes,

            "pet_details": {
                "id": pet.id,
                "name": pet.name,
                "owner_name": pet.user.username if pet.user else None,
                "birth_date": pet.birth_date.strftime("%Y-%m-%d") if pet.birth_date else None,
                "gender": pet.gender,
                "weight": pet.weight,
                "health_condition": getattr(pet, "health_condition", None),
                "category": pet.category.petcategory if pet.category else None,
                "sub_category": pet.sub_category.petsubcategory if pet.sub_category else None,
                "image": pet_image  # relative path: media/...
            },

            "doctor_details": {
                "id": doctor.id,
                "full_name": doctor.full_name,
                "email": doctor.email,
                "phone_number": doctor.phone_number,
                "address": doctor.address,
                "latitude": float(doctor.latitude),
                "longitude": float(doctor.longitude),
                "status": doctor.status,
                "is_approved": doctor.is_approved,
                "image": doctor_image,  # relative path: media/...
                "id_card": doctor_id_card  # relative path: media/...
            }
        }

        return Response(
            {"success": True, "treatment_details": treatment_data},
            status=status.HTTP_200_OK
        )
        

class UpdateDoctorProfileView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):

        doctor_id = request.data.get('doctor_id')
        if not doctor_id:
            return Response(
                {"detail": "Doctor ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response(
                {"detail": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(doctor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "detail": "Doctor profile updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class DoctorFeedbackListView(APIView):

    def get(self, request):
        doctor_id = request.query_params.get("doctor_id")

        if not doctor_id:
            return Response({
                "status": "error",
                "message": "doctor_id is required as a query parameter."
            }, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter(appointment__doctor_id=doctor_id).order_by('-created_at')

        serializer = FeedbackSerializer(feedbacks, many=True)
        
        return Response({
            "status": "success",
            "doctor_id": doctor_id,
            "count": feedbacks.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
class DoctorComplaintListView(APIView):

    def get(self, request):
        doctor_id = request.query_params.get("doctor_id")

        if not doctor_id:
            return Response({
                "status": "error",
                "message": "doctor_id is required as a query parameter."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter complaints where appointment doctor is this doctor
        complaints = Complaint.objects.filter(
            appointment__doctor_id=doctor_id
        ).order_by('-created_at')

        serializer = ComplaintSerializer(complaints, many=True)

        return Response({
            "status": "success",
            "doctor_id": doctor_id,
            "count": complaints.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)